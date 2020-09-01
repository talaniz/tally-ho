"""Main module."""
from collections import namedtuple
import sqlite3


class TallyHo(object):
    """An object to track tallies."""

    def __init__(self, db_name):
        self.db = db_name

    def create_category(self, category):
        """Create a category"""
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute('CREATE TABLE categories (id integer primary key, name varchar)')
        c.execute("insert into categories(name) values (?)", (category,))
        conn.commit()
        c.close()

    def create_tally(self, category, item):
        """Create a tally item under a category."""
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute('''CREATE TABLE tally
        (id integer primary key, name varchar, category integer, count integer,
        FOREIGN KEY (category) REFERENCES categories(id))''')

        c.execute("""SELECT id from categories where name='%s'""" % category)
        category_id = c.fetchone()[0]

        c.execute(
            '''insert into tally(name, category, count) values (?, ?, ?)''', (item, category_id, 1,))
        conn.commit()

    def get_tally(self, tally_name):
        """Retrieve a tally record"""
        Tally = namedtuple("Tally", "id name category count")
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute("SELECT * FROM tally WHERE name='%s'" % tally_name)
        record = c.fetchone()
        tally = Tally(*record)
        return tally
