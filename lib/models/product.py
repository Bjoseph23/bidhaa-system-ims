from models import __init__  # Assuming this imports necessary database connection details

class Product:

    # Dictionary of Product objects saved to the database.
    all = {}

    def __init__(self, name, price, description=""):
        """
        Initialize a new Product instance.

        Args:
            name (str): The name of the product.
            price (float): The price of the product (must be non-negative).
            description (str, optional): A description of the product. Defaults to an empty string.
        """

        self.name = name
        self.price = price
        self.description = description

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
            raise ValueError(
                "Name must be a non-empty string"
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

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        if isinstance(description, str):
            self._description = description
        else:
            raise ValueError(
                "Description must be a string"
            )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Product instances """
        sql = """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  # Added AUTOINCREMENT for automatic ID generation
                name TEXT NOT NULL,
                price REAL NOT NULL,
                description TEXT)
        """
        __init__.CURSOR.execute(sql)
        __init__.CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Product instances """
        sql = """
            DROP TABLE IF EXISTS products;
        """
        __init__.CURSOR.execute(sql)
        __init__.CONN.commit()

    def save(self):
        """ Insert a new row with the name, price, and description values of the current Product instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO products (name, price, description)
            VALUES (?, ?, ?)
        """

        __init__.CURSOR.execute(sql, (self.name, self.price, self.description))
        __init__.CONN.commit()

        self.id = __init__.CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, price, description=""):
        """ Initialize a new Product instance and save the object to the database.
        Returns the created Product object. """
        product = cls(name, price, description)
        product.save()
        return product

    def update(self):
        """Update the table row corresponding to the current Product instance."""
        sql = """
            UPDATE products
            SET name = ?, price = ?, description = ?
            WHERE id = ?
        """
        __init__.CURSOR.execute(sql, (self.name, self.price, self.description, self.id))
        __init__.CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Product instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM products
            WHERE id = ?
        """

        __init__.CURSOR.execute(sql, (self.id,))
        __init__.CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        """Return a Product object having the attribute values from the table row.

        Args:
            row (tuple): A tuple containing the values from a database row for a product.

        Returns:
            Product: A Product object representing the retrieved product data.
        """

        # Check the dictionary for an existing instance using the row's primary key
        product = cls.all.get(row[0])
        if product:
            # Ensure attributes match row values in case local instance was modified
            product.name = row[1]
            product.price = row[2]
            product.description = row[3] if len(row) > 3 else ""  # Handle potential missing description column
        else:
            # Not in dictionary, create new instance and add to dictionary
            product = cls(row[1], row[2], row[3] if len(row) > 3 else "")
            product.id = row[0]
            cls.all[product.id] = product
        return product