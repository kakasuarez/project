def print_table(cursor):
    result = cursor.fetchall()
    for row in result:
        print(row)
        print("\n")


def create_customer(cursor, connection):
    customer_number = 1
    cursor.execute("SELECT MAX(CNO) FROM CUSTOMERS;")
    a = cursor.fetchone()
    last_customer_number = a[0]
    if last_customer_number:
        customer_number = last_customer_number + 1

    name = input("Enter customer name:\n")
    address = input("Enter customer address:\n")
    pno = input("Enter customer phone number:\n")
    if not pno:
        pno = "NULL"
    email = input("Enter customer email:\n")
    password = input("Enter customer password:\n")
    balance = 0

    cursor.execute(
        "INSERT INTO CUSTOMERS VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
            customer_number, name, address, pno, email, password, balance
        )
    )

    connection.commit()
    print("Your customer number is: " + str(customer_number))


def create_item(cursor, connection):
    item_number = 1
    cursor.execute("SELECT MAX(INO) FROM ITEMS;")
    a = cursor.fetchone()
    last_item_number = a[0]
    if last_item_number:
        item_number = last_item_number + 1

    name = input("Enter item name:\n")
    cost = int(input("Enter item cost:\n"))
    stock = int(input("Enter item stock:\n"))
    type = input("Enter item type:\n")

    cursor.execute(
        "INSERT INTO ITEMS VALUES ('{}', '{}', '{}', '{}', '{}')".format(
            item_number, name, cost, stock, type
        )
    )

    connection.commit()


def search_item(item_name, cursor, identifier):

    if identifier not in ("name, type"):
        # error
        return

    cursor.execute(
        "SELECT * FROM ITEMS WHERE {} LIKE '%{}%';".format(identifier, item_name)
    )

    result = cursor.fetchall()

    for row in result:

        stock = "In stock"

        if int(row[3]) < 0:
            # Not in stock
            stock = "Not in stock"

        print()
        print("Item number: ", row[0])
        print("Name: ", row[1])
        print("Price (in ₹): ", row[2])
        print("Stock: ", stock)
        print("Type: ", row[4])
        print("-" * 50)


def view_table(cursor, name):
    """
    Utility function to view any particular table and its entries.
    """
    # cursor.execute("DESC {}".format(name))
    # print_table(cursor)
    cursor.execute("SELECT * FROM %s;" % name)
    print_table(cursor)


def buy_item(item_number, cursor):
    query = "SELECT * FROM ITEMS WHERE INO = {}".format(item_number)
    cursor.execute(query)
    result = cursor.fetchone()
    print("Name: ", result[1])
    print("Cost: ", result[2])
    print("Type: ", result[4])

    confirmation = input("Please confirm if this is the product you want to buy:\n (Y)")
    if confirmation.lower() not in ("yes", "y"):
        return

    quantity = int(input("Please enter the quantity you want to purchase:\n"))
    stock = result[3]
    while quantity > stock:
        print("Stock is only {}. Enter less quantity.".format(stock))
        quantity = int(input("Please enter the quantity you want to purchase:\n"))

    customer_number = int(input("Enter customer number:\n"))
    balance = 0
    cursor.execute(
        "SELECT BALANCE FROM CUSTOMERS WHERE CNO = {};".format(customer_number)
    )
    cursor.fetchone()
    print(result)
