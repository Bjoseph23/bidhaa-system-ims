from models.__init__ import CURSOR, CONN

class Product:

    all = {}

    def __init__(self, name, price, description="", category_id=None):
        self.name = name
        self.price = price
        self.description = description
        self.category_id = category_id

    def __repr__(self):
        return f"<Product {self.id}: {self.name}>"

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
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if isinstance(price, (int, float)) and price >= 0:
            self._price = price
        else:
            raise ValueError("Price must be a non-negative number")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        if isinstance(description, str):
            self._description = description
        else:
            raise ValueError("Description must be a string")

    @property
    def category_id(self):
        return self._category_id

    @category_id.setter
    def category_id(self, category_id):
        if category_id is None or isinstance(category_id, int):
            self._category_id = category_id
        else:
            raise ValueError("category_id must be an integer or None")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            category_id INTEGER REFERENCES categories(id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS products"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = "INSERT INTO products (name, price, description, category_id) VALUES (?, ?, ?, ?)"
        CURSOR.execute(sql, (self.name, self.price, self.description, self.category_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, price, description="", category_id=None):
        product = cls(name, price, description, category_id)
        product.save()
        return product

    def update(self):
        sql = "UPDATE products SET name = ?, price = ?, description = ?, category_id = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.price, self.description, self.category_id, self.id))
        CONN.commit()

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM products"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id_):
        sql = "SELECT * FROM products WHERE id = ?"
        CURSOR.execute(sql, (id_,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM products WHERE name = ?"
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

    def delete(self):
        sql = "DELETE FROM products WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        product = cls.all.get(row[0])
        if product:
            product.name = row[1]
            product.price = row[2]
            product.description = row[3] if len(row) > 3 else ""
            product.category_id = row[4] if len(row) > 4 else None
        else:
            product = cls(row[1], row[2], row[3] if len(row) > 3 else "", row[4] if len(row) > 4 else None)
            product.id = row[0]
            cls.all[product.id] = product
        return product
