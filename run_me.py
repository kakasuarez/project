from startup import connect, create_database, get_cursor

from table_handling import (
    create_customer,
    create_item,
    search_item,
    view_table,
    buy_item,
)

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


print("1.Create customer 2.Search for item 3.Buy item")

if is_admin:
    print("4.View tables 5.Add item")

option = int(input("Enter your choice="))

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
    buy_item(item_number, cursor)

elif option == 4 and is_admin:
    name = input("Enter table name to view")
    view_table(cursor, name)

elif option == 5 and is_admin:
    create_item(cursor, connection)
