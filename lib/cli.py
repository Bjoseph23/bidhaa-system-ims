from helpers import (
    exit_program,
    list_suppliers,
    find_supplier_by_name,
    find_supplier_by_id,
    create_supplier,
    update_supplier,
    delete_supplier,
    list_products,
    find_product_by_name,
    find_product_by_id,
    create_product,
    update_product,
    delete_product,
    list_order_history,
    find_order_history_by_id,
    create_order_history,
    update_order_history,
    delete_order_history,
    list_order_details,
    find_order_details_by_id,
    create_order_details,
    update_order_details,
    delete_order_details,
    list_categories,
    find_category_by_name,
    find_category_by_id,
    create_category,
    update_category,
    delete_category,
)

def main():
    while True:
        menu()
        choice = input("Enter choice:  ")
        if choice == "0":
            exit_program()

        # Supplier options
        if choice in ("1", "2", "3", "4", "5", "6"):
            supplier_functions(choice)

        # Product options
        elif choice in ("7", "8", "9", "10", "11", "12"):
            product_functions(choice)

        # Order history options
        elif choice in ("13", "14", "15", "16", "17"):
            order_history_functions(choice)

        # Order details options
        elif choice in ("18", "19", "20", "21", "22"):
            order_details_functions(choice)

        # Category options
        elif choice in ("23", "24", "25", "26", "27", "28"):
            category_functions(choice)

        else:
            print("Invalid choice")


def menu():
    print("Please select an option:")
    print("0. Exit the program")

    # Supplier options
    print("\nSupplier Management:")
    print("1. List all suppliers")
    print("2. Find supplier by name")
    print("3. Find supplier by id")
    print("4. Create supplier")
    print("5. Update supplier")
    print("6. Delete supplier")

    # Product options
    print("\nProduct Management:")
    print("7. List all products")
    print("8. Find product by name")
    print("9. Find product by id")
    print("10. Create product")
    print("11. Update product")
    print("12. Delete product")

    # Order history options
    print("\nOrder History Management:")
    print("13. List all order history")
    print("14. Find order history by id")
    print("15. Create order history")
    print("16. Update order history")
    print("17. Delete order history")

    # Order details options
    print("\nOrder Details Management:")
    print("18. List all order details")
    print("19. Find order details by id")
    print("20. Create order details")
    print("21. Update order details")
    print("22. Delete order details")

    # Category options
    print("\nCategory Management:")
    print("23. List all categories")
    print("24. Find category by name")
    print("25. Find category by id")
    print("26. Create category")
    print("27. Update category")
    print("28. Delete category")


def supplier_functions(choice):
    if choice == "1":
        list_suppliers()
    elif choice == "2":
        find_supplier_by_name()
    elif choice == "3":
        find_supplier_by_id()
    elif choice == "4":
        create_supplier()
    elif choice == "5":
        update_supplier()
    elif choice == "6":
        delete_supplier()

def product_functions(choice):
    if choice == "7":
        list_products()
    elif choice == "8":
        find_product_by_name()
    elif choice == "9":
        find_product_by_id()
    elif choice == "10":
        create_product()
    elif choice == "11":
        update_product()
    elif choice == "12":
        delete_product()

def order_history_functions(choice):
    if choice == "13":
        list_order_history()
    elif choice == "14":
        find_order_history_by_id()
    elif choice == "15":
        create_order_history()
    elif choice == "16":
        update_order_history()
    elif choice == "17":
        delete_order_history()

def order_details_functions(choice):
    if choice == "18":
        list_order_details()
    elif choice == "19":
        find_order_details_by_id()
    elif choice == "20":
        create_order_details()
    elif choice == "21":
        update_order_details()
    elif choice == "22":
        delete_order_details()

def category_functions(choice):
    if choice == "23":
        list_categories()
    elif choice == "24":
        find_category_by_name()
    elif choice == "24":
        find_category_by_name()
    elif choice == "25":
        find_category_by_id()
    elif choice == "26":
        create_category()
    elif choice == "27":
        update_category()
    elif choice == "28":
        delete_category()


if __name__ == "__main__":
    main()