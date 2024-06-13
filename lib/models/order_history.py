from models.__init__ import CURSOR, CONN
from models.product import Product

class OrderHistory:

    all = {}

    def __init__(self, product, quantity, order_date, id=None):
        self.id = id
        self.product = product
        self.quantity = quantity
        self.order_date = order_date

    def __repr__(self):
        return f"<OrderHistory {self.id}: {self.product.name}, {self.quantity}>"

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, product):
        if isinstance(product, Product):
            self._product = product
        else:
            raise ValueError("Product must be a Product object")

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        if isinstance(quantity, int) and quantity > 0:
            self._quantity = quantity
        else:
            raise ValueError("Quantity must be a positive integer")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS order_history (
            id INTEGER PRIMARY KEY,
            product_id INTEGER REFERENCES products(id),
            quantity INTEGER,
            order_date TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS order_history
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO order_history (product_id, quantity, order_date) VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.product.id, self.quantity, self.order_date))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, product, quantity, order_date):
        order = cls(product, quantity, order_date)
        order.save()
        return order

    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM order_history
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def instance_from_db(cls, row):
        order = cls.all.get(row[0])
        if order:
            order.product = Product.find_by_id(row[1])
            order.quantity = row[2]
            order.order_date = row[3]
        else:
            order = cls(Product.find_by_id(row[1]), row[2], row[3])
            order.id = row[0]
            cls.all[order.id] = order
        return order

    @classmethod
    def find_by_id(cls, id_):
        sql = """
            SELECT * FROM products WHERE id = ?
        """
        CURSOR.execute(sql, (id_,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
