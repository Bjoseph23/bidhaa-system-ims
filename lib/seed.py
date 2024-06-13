from models.product import Product
from models.supplier import Supplier
from models.order_detail import OrderDetails
from models.order_history import OrderHistory
from models.category import Category

def seed_database():
    # Drop existing tables
    Product.drop_table()
    Supplier.drop_table()
    OrderDetails.drop_table()
    OrderHistory.drop_table()
    Category.drop_table()

    # Create tables
    Product.create_table()
    Supplier.create_table()
    OrderDetails.create_table()
    OrderHistory.create_table()
    Category.create_table()

    # Seed data
    seed_products()
    seed_suppliers()
    seed_order_history()
    seed_order_details()
    seed_categories()

    print("Seeded database")

def seed_products():
    product1 = Product.create("Laptop", 1000.00, "High-performance laptop",1)
    product2 = Product.create("T-Shirt", 20.00, "Comfortable and stylish T-shirt",2)

def seed_suppliers():
    supplier1 = Supplier.create("TechGiant Inc.", "123 Main St")
    supplier2 = Supplier.create("Fashion Emporium", "456 Elm St")

def seed_order_history():
    product1 = Product.find_by_id(1)
    product2 = Product.find_by_id(2)

    if product1 and product2:
        order_history1 = OrderHistory.create(product1, 2, "2024-06-10")
        order_history2 = OrderHistory.create(product2, 5, "2024-06-11")
    else:
        print("Error: Product not found")


def seed_order_details():
    product1 = Product.find_by_id(1)
    supplier1 = Supplier.find_by_id(1)
    product2 = Product.find_by_id(2)
    supplier2 = Supplier.find_by_id(2)

    if product1 and supplier1 and product2 and supplier2:
        order_detail1 = OrderDetails.create(product1, supplier1, 2, "2024-06-10")
        order_detail2 = OrderDetails.create(product2, supplier2, 5, "2024-06-11")
    else:
        print("Error: Product or Supplier not found")

def seed_categories():
    category1 = Category.create("Electronics")
    category2 = Category.create("Clothing")

if __name__ == "__main__":
    seed_database()
