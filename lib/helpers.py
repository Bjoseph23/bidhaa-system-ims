from lib.models.product import Product, Category
from lib.models.category import Supplier 
from lib.models.order_history import OrderHistory
from lib.models.order_detail import OrderDetails


def exit_program():
    print("Goodbye!")
    exit()


# Supplier functions
def list_suppliers():
    suppliers = Supplier.get_all()
    for supplier in suppliers:
        print(supplier)


def find_supplier_by_name():
    name = input("Enter the supplier's name: ")
    supplier = Supplier.find_by_name(name)
    print(supplier) if supplier else print(f'Supplier {name} not found')


def find_supplier_by_id():
    id_ = input("Enter the supplier's id: ")
    supplier = Supplier.find_by_id(id_)
    print(supplier) if supplier else print(f'Supplier {id_} not found')


def create_supplier():
    name = input("Enter the supplier's name: ")
    contact_info = input("Enter the supplier's contact information (optional): ")
    try:
        supplier = Supplier.create(name, contact_info)
        print(f'Success: {supplier}')
    except Exception as exc:
        print("Error creating supplier: ", exc)


def update_supplier():
    id_ = input("Enter the supplier's id: ")
    if supplier := Supplier.find_by_id(id_):
        try:
            name = input("Enter the supplier's new name: ")
            supplier.name = name
            contact_info = input("Enter the supplier's new contact information (optional): ")
            supplier.contact_info = contact_info
            supplier.update()
            print(f'Success: {supplier}')
        except Exception as exc:
            print("Error updating supplier: ", exc)
    else:
        print(f'Supplier {id_} not found')


def delete_supplier():
    id_ = input("Enter the supplier's id: ")
    if supplier := Supplier.find_by_id(id_):
        supplier.delete()
        print(f'Supplier {id_} deleted')
    else:
        print(f'Supplier {id_} not found')


# Product functions
def list_products():
    products = Product.get_all()
    for product in products:
        print(product)


def find_product_by_name():
    name = input("Enter the product's name: ")
    product = Product.find_by_name(name)
    print(product) if product else print(f'Product {name} not found')


def find_product_by_id():
    id_ = input("Enter the product's id: ")
    product = Product.find_by_id(id_)
    print(product) if product else print(f'Product {id_} not found')


def create_product():
    name = input("Enter the product's name: ")
    price = float(input("Enter the product's price: "))
    category_name = input("Enter the product's category name: ")
    category = Category.find_by_name(category_name)
    if not category:
        print(f'Category {category_name} not found. Please create the category first.')
        return
    try:
        product = Product.create(name, price, category)
        print(f'Success: {product}')
    except Exception as exc:
        print("Error creating product: ", exc)


def update_product():
    id_ = input("Enter the product's id: ")
    if product := Product.find_by_id(id_):
        try:
            name = input("Enter the product's new name: ")
            product.name = name
            price = float(input("Enter the product's new price: "))
            product.price = price
            category_name = input("Enter the product's category name (optional): ")
            if category_name:
                category = Category.find_by_name(category_name)
                if not category:
                    print(f'Category {category_name} not found.')
                else:
                    product.category = category
            product.update()
            print(f'Success: {product}')
        except Exception as exc:
            print("Error updating product: ", exc)
    else:
        print(f'Product {id_} not found')


def delete_product():
    id_ = input("Enter the product's id: ")
    if product := Product.find_by_id(id_):
        product.delete()
        print(f'Product {id_} deleted')
    else:
        print(f'Product {id_} not found')


# Order history functions
def list_order_history():
    order_history = OrderHistory.get_all()
    for order in order_history:
        print(order)


def find_order_history_by_id():
    id_ = input("Enter the order history's id: ")
    order_history = OrderHistory.find_by_id(id_)
    print(order_history) if order_history else print(f'Order history {id_} not found')


def create_order_history():
    product_id = int(input("Enter the product's id: "))
    if not Product.find_by_id(product_id):
        print(f'Product with id {product_id} not found.')
        return
    quantity = int(input("Enter the order quantity: "))
    order_date = input("Enter the order date (YYYY-MM-DD): ")
    try:
        order_history = OrderHistory.create(Product(product_id), quantity, order_date)
        print(f'Success: {order_history}')
    except Exception as exc:
        print("Error creating order history: ", exc)


def update_order_history():
    id_ = input("Enter the order history's id: ")
    if order_history := OrderHistory.find_by_id(id_):
        try:
            product_id = int(input("Enter the product's new id (optional): "))
            if product_id:
                if not Product.find_by_id(product_id):
                    print(f'Product with id {product_id} not found.')
                    return
                order_history.product = Product(product_id)
            quantity = int(input("Enter the order quantity (optional): "))
            if quantity > 0:
                order_history.quantity = quantity
            order_date = input("Enter the new order date (YYYY-MM-DD) (optional): ")
            if order_date:
                order_history.order_date = order_date
            order_history.update()
            print(f'Success: {order_history}')
        except Exception as exc:
            print("Error updating order history: ", exc)
    else:
        print(f'Order history {id_} not found')


def delete_order_history():
    id_ = input("Enter the order history's id: ")
    if order_history := OrderHistory.find_by_id(id_):
        order_history.delete()
        print(f'Order history {id_} deleted')
    else:
        print(f'Order history {id_} not found')


# Order details functions
def list_order_details():
    order_details = OrderDetails.get_all()
    for detail in order_details:
        print(detail)


def find_order_details_by_id():
    id_ = input("Enter the order detail's id: ")
    order_detail = OrderDetails.find_by_id(id_)
    print(order_detail) if order_detail else print(f'Order detail {id_} not found')


def create_order_details():
    order_history_id = int(input("Enter the order history's id: "))
    if not OrderHistory.find_by_id(order_history_id):
        print(f'Order history with id {order_history_id} not found.')
        return
    quantity = int(input("Enter the order quantity: "))
    price = float(input("Enter the product's price: "))
    try:
        order_detail = OrderDetails.create(
            OrderHistory(order_history_id), quantity, price
        )
        print(f'Success: {order_detail}')
    except Exception as exc:
        print("Error creating order detail: ", exc)

def update_order_details():
    id_ = input("Enter the order detail's id: ")
    if order_detail := OrderDetails.find_by_id(id_):
        try:
            order_history_id = int(input("Enter the order history's new id (optional): "))
            if order_history_id:
                if not OrderHistory.find_by_id(order_history_id):
                    print(f'Order history with id {order_history_id} not found.')
                    return
                order_detail.order_history = OrderHistory(order_history_id)
            quantity = int(input("Enter the order quantity (optional): "))
            if quantity > 0:
                order_detail.quantity = quantity
            price = float(input("Enter the product's new price (optional): "))
            if price >= 0:
                order_detail.price = price
            order_detail.update()
            print(f'Success: {order_detail}')
        except Exception as exc:
            print("Error updating order detail: ", exc)
    else:
        print(f'Order detail {id_} not found')


def delete_order_details():
    id_ = input("Enter the order detail's id: ")
    if order_detail := OrderDetails.find_by_id(id_):
        order_detail.delete()
        print(f'Order detail {id_} deleted')
    else:
        print(f'Order detail {id_} not found')


# Category functions (assuming Category is a separate table)
def list_categories():
    categories = Category.get_all()
    for category in categories:
        print(category)


def find_category_by_name():
    name = input("Enter the category's name: ")
    category = Category.find_by_name(name)
    print(category) if category else print(f'Category {name} not found')


def find_category_by_id():
    id_ = input("Enter the category's id: ")
    category = Category.find_by_id(id_)
    print(category) if category else print(f'Category {id_} not found')


def create_category():
    name = input("Enter the category's name: ")
    try:
        category = Category.create(name)
        print(f'Success: {category}')
    except Exception as exc:
        print("Error creating category: ", exc)


def update_category():
    id_ = input("Enter the category's id: ")
    if category := Category.find_by_id(id_):
        try:
            name = input("Enter the category's new name: ")
            category.name = name
            category.update()
            print(f'Success: {category}')
        except Exception as exc:
            print("Error updating category: ", exc)
    else:
        print(f'Category {id_} not found')


def delete_category():
    id_ = input("Enter the category's id: ")
    if category := Category.find_by_id(id_):
        category.delete()
        print(f'Category {id_} deleted')
    else:
        print(f'Category {id_} not found')