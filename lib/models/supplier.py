from models.__init__ import CURSOR, CONN

class Supplier:

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
            raise ValueError("Name must be a non-empty string")

    @property
    def contact_info(self):
        return self._contact_info

    @contact_info.setter
    def contact_info(self, contact_info):
        if isinstance(contact_info, str):
            self._contact_info = contact_info
        else:
            raise ValueError("Contact information must be a string")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            contact_info TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()


    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS suppliers
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO suppliers (name, contact_info) VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.contact_info))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, contact_info=""):
        supplier = cls(name, contact_info)
        supplier.save()
        return supplier

    def update(self):
        sql = """
            UPDATE suppliers SET name = ?, contact_info = ? WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.contact_info, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM suppliers WHERE id = ?
            """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        supplier = cls.all.get(row[0])
        if supplier:
            supplier.name = row[1]
            supplier.contact_info = row[2] if len(row) > 2 else ""
        else:
            supplier = cls(row[1], row[2] if len(row) > 2 else "")
            supplier.id = row[0]
            cls.all[supplier.id] = supplier
        return supplier

    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM suppliers
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id_):
        sql = """
            SELECT * FROM suppliers WHERE id = ?
        """
        CURSOR.execute(sql, (id_,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
