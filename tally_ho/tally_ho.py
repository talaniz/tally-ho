"""This module is the transaction interface between the cli and the database."""
from collections import namedtuple
import sqlite3

from tally_ho.exceptions import DuplicateCategoryException, DuplicateTallyException


Tally = namedtuple("Tally", "id name category count")
Category = namedtuple("Category", "id name")


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
            raise DuplicateCategoryException("Another record with this name already exists")
        c.execute("SELECT * FROM categories WHERE name='%s'" % category)
        record = c.fetchone()
        c.close()
        return Category(*record)

    def create_tally(self, category, item):
        """Create a tally item under a category."""
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tally
        (id integer primary key, name varchar, category integer, count integer,
        FOREIGN KEY (category) REFERENCES categories(id))''')

        tally = self.get_tally(item)

        if tally == '':
            c.execute("""SELECT id from categories where name='%s'""" % category)
            category_id = c.fetchone()[0]

            c.execute(
                '''insert into tally(name, category, count) values (?, ?, ?)''', (item, category_id, 1,))
            conn.commit()
            return self.get_tally(item)
        else:
            raise DuplicateTallyException("Existing Tally:\n\tName: {}\n\tCategory: {}\n\tCount: {}".format(tally.name, tally.category, category.count))

    def get_tally(self, tally_name):
        """Retrieve a tally record"""
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute("SELECT * FROM tally WHERE name='%s'" % tally_name)
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

    def update_tally(self, tally_name, interval):
        """Increase or decrease count on a tally."""
        tally = self.get_tally(tally_name)
        count = tally.count + interval
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute("""UPDATE tally SET count = ? where id= ?""",
                  (count, tally.id,))
        conn.commit()
        return self.get_tally(tally_name)

    def delete_tally(self, category, item):
        """Delete the tally record"""
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute("DELETE FROM tally WHERE name='%s'" % item)
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
