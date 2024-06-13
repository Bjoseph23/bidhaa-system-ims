#!/usr/bin/env python3

from models.product import Product
from models.supplier import Supplier
from models.order_detail import OrderDetails
from models.order_history import OrderHistory
from models.category import Category

def seed_database():
    # Drop any existing tables (optional, comment out if not desired)
    Product.drop_table()
    Supplier.drop_table()
    OrderDetails.drop_table()
    OrderHistory.drop_table()
    Category.drop_table()

    Product.create_table()
    Supplier.create_table()
    OrderDetails.create_table()
    OrderHistory.create_table()
    Category.create_table()

    # Seed data (replace with your actual data)
    category1 = Category.create("Electronics")
    category2 = Category.create("Clothing")

    product1 = Product.create(
        "Laptop", 1000.00, "This is a high-performance laptop", category1.id
    )
    product2 = Product.create(
        "T-Shirt", 20.00, "Comfortable and stylish T-shirt", category2.id
    )

    supplier1 = Supplier.create("TechGiant Inc.", "123 Main St")
    supplier2 = Supplier.create("Fashion Emporium", "456 Elm St")

    order_history1 = OrderHistory.create(product1.id, 2, "2024-06-10")
    order_detail1 = OrderDetails.create(order_history1.id, 500.00)

    order_history2 = OrderHistory.create(product2.id, 5, "2024-06-11")
    order_detail2 = OrderDetails.create(order_history2.id, 10.00)

    # Add more seed data as needed for other tables

seed_database()
print("Seeded database")
