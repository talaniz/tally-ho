"""Main module."""
import sqlite3


class TallyHo(object):
    """An object to track tallies."""

    def create_category(self, category, db_name):
        """Create a category"""
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute('CREATE TABLE categories (id integer primary key, name varchar)')
        c.execute("insert into categories(name) values (?)", (category,))
        conn.commit()
        c.close()
        print("Category: {} created\n".format(category))

    def create_tally(self, category, item, db_name):
        """Create a tally item under a category."""
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE tally
        (id integer primary key, name varchar, category integer, count integer,
        FOREIGN KEY (category) REFERENCES categories(id))''')

        c.execute("""SELECT id from categories where name='%s'""" % category)
        category_id = c.fetchone()[0]

        c.execute(
            '''insert into tally(name, category, count) values (?, ?, ?)''', (item, category_id, 1,))
        conn.commit()
        print("Created tally '{}' under '{}'\nCurrent tally: 1".format(item, category))
