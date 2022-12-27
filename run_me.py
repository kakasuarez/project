"""
File which is the main file to be run by the end user.
It contains the menu for the program.
"""

from startup import connect, create_database, get_cursor

from table_handling import (
    create_customer,
    create_item,
    search_item,
    view_table,
    buy_item,
    add_balance,
    view_customer_details,
    edit_customer_details,
    add_stock,
)

from file_handling import read_file, get_monthly_revenue

from password_handling import ask_for_admin

connection = connect()
cursor = get_cursor(connection)
create_database(cursor)

option = None

choice = None

while choice not in ("Y", "N"):
    choice = input("Do you want to login as admin? (Y or N)\n")
    choice = choice.upper()

if choice == "N":
    is_admin = False

if choice == "Y":
    is_admin = ask_for_admin()

option = 1
while option != 0:

    print("1.Create customer\n2.Search for item\n3.Buy item")
    if is_admin:
        print(
            "4.View tables\n5.Add item\n6.Add Balance\n7.View Customer details\n8.Edit customer details\n9.View orders\n10.View monthly revenue\n11.Add stock"
        )
    option = int(input("Enter your choice (0 for exit):\n"))

    if option == 1:
        create_customer(cursor, connection)

    elif option == 2:
        item_name = ""
        search_choice = int(
            input(
                "Do you want to search by name or type? Enter 1 for name and 2 for type.\n"
            )
        )
        if search_choice == 1:
            identifier = "name"
            item_name = input("Enter item name you want to search:\n")
            search_item(item_name, cursor, identifier)
        elif search_choice == 2:
            identifier = "type"
            item_name = input("Enter type of item you want to search:\n")
            search_item(item_name, cursor, identifier)
        else:
            print("Incorrect option.")

    elif option == 3:
        item_number = int(
            input("Enter the item number of the item you want to purchase:\n")
        )
        buy_item(item_number, cursor, connection)

    elif option == 4 and is_admin:
        name = input("Enter table name to view:\n")
        view_table(cursor, name)

    elif option == 5 and is_admin:
        create_item(cursor, connection)

    elif option == 6 and is_admin:
        customer_number = int(input("Enter customer number:\n"))
        bal = int(input("Enter amount of balance to be added:\n"))
        add_balance(bal, customer_number, cursor, connection)

    elif option == 7 and is_admin:
        customer_number = input(
            "Enter the customer number of customer whose details you want to see:\n"
        )
        view_customer_details(customer_number, cursor)

    elif option == 8 and is_admin:
        customer_number = input(
            "Enter the customer number of customer whose details you want to edit:\n"
        )
        edit_customer_details(customer_number, cursor)
    elif option == 9 and is_admin:
        read_file(cursor)

    elif option == 10 and is_admin:
        get_monthly_revenue(cursor)

    elif option == 11 and is_admin:
        item_number = int(input("Enter item number:\n"))
        stock = int(input("Enter additional stock:\n"))
        add_stock(stock, item_number, cursor, connection)
