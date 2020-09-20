"""Module for database reads and writes."""
from collections import namedtuple
import sqlite3

from tally_ho.exceptions import (
    DuplicateCategoryException,
    DuplicateTallyException
)


class Tally(namedtuple("Tally", ["id", "name", "category", "count"])):
    """A tally record."""

    def __str__(self):
        return "Name: {} Category: {} Count: {}".format(self.name,
                                                        self.category,
                                                        self.count)


class Category(namedtuple("Category", ["id", "name"])):
    """A category to assign events."""
    def __str__(self):
        return "Name: {}".format(self.name)


class TallyHo(object):
    """An object to track tallies."""

    def __init__(self, db_name):
        self.db = db_name

    def create_category(self, category):
        """Create a category"""
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS categories (id integer primary key, name varchar, UNIQUE (name))')

        try:
            c.execute("insert into categories(name) values (?)", (category,))
            conn.commit()
        except sqlite3.IntegrityError:
            raise DuplicateCategoryException("Record already exists")
        c.execute("SELECT * FROM categories WHERE name='%s'" % category)
        record = c.fetchone()
        c.close()
        return Category(*record)

    def create_tally(self, category, name):
        """Create a tally name under a category."""
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tally
        (id integer primary key, name varchar, category integer, count integer,
        FOREIGN KEY (category) REFERENCES categories(id))''')

        tally_cat = self.get_category(category)
        tally = self.get_tally(name, category)

        if (tally == '') or (tally.category != tally_cat.id):
            c.execute(
                '''insert into tally(name, category, count) values (?, ?, ?)''', (name,
                                                                                  tally_cat.id,
                                                                                  1,))
            conn.commit()
            conn.close()
            return self.get_tally(name, category)
        else:
            raise DuplicateTallyException("Existing Tally:\n\tName: {}\n\tCategory: {}\n\tCount: {}".format(tally.name, tally.category, category.count))

    def get_tally(self, tally_name, category):
        """Retrieve a tally record"""
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        cat = self.get_category(category)
        c.execute("SELECT * FROM tally WHERE name=? AND category=?", (tally_name, cat.id,))
        record = c.fetchone()

        if record:
            tally = Tally(*record)
            return tally
        return ''

    def get_tallies(self):
        """Return all tallies"""
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute('SELECT * FROM tally')
        return [Tally(*record) for record in c.fetchall()]

    def update_tally(self, tally_name, tally_category, interval):
        """Increase or decrease count on a tally."""
        tally = self.get_tally(tally_name, tally_category)
        count = tally.count + interval
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute("""UPDATE tally SET count = ? where id= ?""",
                  (count, tally.id,))
        conn.commit()
        return self.get_tally(tally_name, tally_category)

    def delete_tally(self, category, tally_name):
        """Delete the tally record"""
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute("DELETE FROM tally WHERE name='%s'" % tally_name)
        conn.commit()

    def get_category(self, category):
        """Get a category record"""
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute("SELECT * FROM categories WHERE name='%s'" % category)
        record = c.fetchone()
        if record:
            return Category(*record)
        return ''

    def get_categories(self):
        """Return all categories"""
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute("SELECT * FROM categories")
        categories = [Category(*record) for record in c.fetchall()]
        return categories

    def delete_category(self, category):
        """Delete the category record"""
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute("DELETE FROM categories WHERE name='%s'" % category)
        conn.commit()
        return self.get_categories()
