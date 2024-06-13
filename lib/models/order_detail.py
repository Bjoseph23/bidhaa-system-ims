from models.__init__ import CURSOR, CONN
from models.product import Product
from models.supplier import Supplier

class OrderDetails:

    all = {}

    def __init__(self, product, supplier, quantity, order_date, id=None):
        self.id = id
        self.product = product
        self.supplier = supplier
        self.quantity = quantity
        self.order_date = order_date

    def __repr__(self):
        return f"<OrderDetails {self.id}: {self.product.name} from {self.supplier.name}, {self.quantity}>"

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
    def supplier(self):
        return self._supplier

    @supplier.setter
    def supplier(self, supplier):
        if isinstance(supplier, Supplier):
            self._supplier = supplier
        else:
            raise ValueError("Supplier must be a Supplier object")

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
            CREATE TABLE IF NOT EXISTS order_details (
            id INTEGER PRIMARY KEY,
            product_id INTEGER REFERENCES products(id),
            supplier_id INTEGER REFERENCES suppliers(id),
            quantity INTEGER,
            order_date TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS order_details
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO order_details (product_id, supplier_id, quantity, order_date) VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.product.id, self.supplier.id, self.quantity, self.order_date))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, product, supplier, quantity, order_date):
        order = cls(product, supplier, quantity, order_date)
        order.save()
        return order

    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM order_details
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def instance_from_db(cls, row):
        order = cls.all.get(row[0])
        if order:
            order.product = Product.find_by_id(row[1])
            order.supplier = Supplier.find_by_id(row[2])
            order.quantity = row[3]
            order.order_date = row[4]
        else:
            order = cls(Product.find_by_id(row[1]), Supplier.find_by_id(row[2]), row[3], row[4])
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