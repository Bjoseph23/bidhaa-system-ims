from models.__init__ import CURSOR, CONN


class Supplier:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, name, contact_info="", id=None):
        self.id = id
        self.name = name
        self.contact_info = contact_info

    def __repr__(self):
        return f"<Supplier {self.id}: {self.name}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )

    @property
    def contact_info(self):
        return self._contact_info

    @contact_info.setter
    def contact_info(self, contact_info):
        if isinstance(contact_info, str):
            self._contact_info = contact_info
        else:
            raise ValueError(
                "Contact information must be a string"
            )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Supplier instances """
        sql = """
            CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            contact_info TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Supplier instances """
        sql = """
            DROP TABLE IF EXISTS suppliers;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name and contact info values of the current Supplier instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO suppliers (name, contact_info)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.contact_info))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, contact_info=""):
        """ Initialize a new Supplier instance and save the object to the database """
        supplier = cls(name, contact_info)
        supplier.save()
        return supplier

    def update(self):
        """Update the table row corresponding to the current Supplier instance."""
        sql = """
            UPDATE suppliers
            SET name = ?, contact_info = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.contact_info, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Supplier instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM suppliers
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        """Return a Supplier object having the attribute values from the table row."""

        # Check the dictionary for an existing instance using the row's primary key
        supplier = cls.all.get(row[0])
        if supplier:
            # ensure attributes match row values in case local instance was modified
            supplier.name = row[1]
            supplier.contact_info = row[2] if len(row) > 2 else ""
        else:
            # not in dictionary, create new instance and add to dictionary
            supplier = cls(row[1], row[2] if len(row) > 2 else "")
            supplier.id = row[0]
            cls.all[supplier.id] = supplier
        return supplier

    @classmethod
    def get_all(cls):
        """Return a list containing a Supplier object per row in the table"""
        sql = """
            SELECT *
            FROM suppliers
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
