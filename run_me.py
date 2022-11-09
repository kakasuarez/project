from startup import connect, create_database, get_cursor, view_table, ask_for_admin

from table_handling import create_customer, create_item


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
    # search_for_item(item_name)
    pass
elif option == 3:
    pass
    # buy_item(item_name)
elif option == 4 and is_admin:
    name = input("Enter table name to view")
    view_table(cursor, name)

elif option == 5 and is_admin:
    create_item(cursor, connection)
