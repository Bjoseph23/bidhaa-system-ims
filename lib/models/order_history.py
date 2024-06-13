from models.__init__ import CURSOR, CONN
from models.product import Product


class OrderHistory:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, product: Product, quantity, order_date, id=None):
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
            raise ValueError(
                "Product must be a Product object"
            )

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        if isinstance(quantity, int) and quantity > 0:
            self._quantity = quantity
        else:
            raise ValueError(
                "Quantity must be a positive integer"
            )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of OrderHistory instances """
        sql = """
            CREATE TABLE IF NOT EXISTS order_history (
            id INTEGER PRIMARY KEY,
            product_id INTEGER REFERENCES products(id),
            quantity INTEGER,
            order_date TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists OrderHistory instances """
        sql = """
            DROP TABLE IF EXISTS order_history;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with product_id, quantity, and order_date values of the current OrderHistory instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO order_history (product_id, quantity, order_date)
            VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.product.id, self.quantity, self.order_date))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, product: Product, quantity, order_date):
        """ Initialize a new OrderHistory instance and save the object to the database """
        order_history = cls(product, quantity, order_date)
        order_history.save()
        return order_history

    def update(self):
        """Update the table row corresponding to the current OrderHistory instance."""
        sql = """
            UPDATE order_history
            SET product_id = ?, quantity = ?, order_date = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.product.id, self.quantity, self.order_date, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current OrderHistory instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM order_history
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
        """Return an OrderHistory object having the attribute values from the table row."""

        # Retrieve the product object using the product_id
        product = Product.find_by_id(row[1])

        # Check the dictionary for an existing instance using the row's primary key
        order_history = cls.all.get(row[0])
        if order_history:
            # ensure attributes match row values in case local instance was modified
            order_history.product = product
            order_history.quantity = row[2]
            order_history.order_date = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            order_history = cls(product, row[2], row[3])
            order_history.id = row[0]
            cls.all[order_history.id] = order_history
        return order_history

