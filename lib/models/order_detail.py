from models.__init__ import CURSOR, CONN
from models.product import Product
from models.order_history import OrderHistory  # Assuming OrderHistory model exists

class OrderDetails:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, order_history: OrderHistory, quantity, price, id=None):
        self.id = id
        self.order_history = order_history
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"<OrderDetails {self.id}: {self.order_history.product.name}, {self.quantity}>"

    @property
    def order_history(self):
        return self._order_history

    @order_history.setter
    def order_history(self, order_history):
        if isinstance(order_history, OrderHistory):
            self._order_history = order_history
        else:
            raise ValueError(
                "Order history must be an OrderHistory object"
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

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if isinstance(price, (int, float)) and price >= 0:
            self._price = price
        else:
            raise ValueError(
                "Price must be a non-negative number"
            )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of OrderDetails instances """
        sql = """
            CREATE TABLE IF NOT EXISTS order_details (
            id INTEGER PRIMARY KEY,
            order_history_id INTEGER REFERENCES order_history(id),
            quantity INTEGER,
            price REAL)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists OrderDetails instances """
        sql = """
            DROP TABLE IF EXISTS order_details;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with order_history_id, quantity, and price values of the current OrderDetails instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO order_details (order_history_id, quantity, price)
            VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.order_history.id, self.quantity, self.price))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, order_history: OrderHistory, quantity, price):
        """ Initialize a new OrderDetails instance and save the object to the database """
        order_details = cls(order_history, quantity, price)
        order_details.save()
        return order_details

    def update(self):
        """Update the table row corresponding to the current OrderDetails instance."""
        sql = """
            UPDATE order_details
            SET order_history_id = ?, quantity = ?, price = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.order_history.id, self.quantity, self.price, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current OrderDetails instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM order_details
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
        """Return an OrderDetails object having the attribute values from the table row."""

        # Retrieve the order history object using the order_history_id
        order_history = OrderHistory.find_by_id(row[1])

        # Check the dictionary for an existing instance using the row's primary key
        order_details = cls.all.get(row[0])
        if order_details:
            # ensure attributes match row values in case local instance was modified
            order_details.order_history = order_history
            order_details.quantity = row[2]
            order_details.price = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            order_details = cls(order_history, row[2], row[3])
            order_details.id = row[0]
            cls.all[order_details.id] = order_details
        return order_details
