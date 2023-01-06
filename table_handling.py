"""
File which deals with all the procedures related to the MySQL database.
The database contains the details of the customers and items.
"""

from datetime import date
from file_handling import add_to_file


def print_table(cursor):
    """
    Function that prints the result of a query.
    """
    result = cursor.fetchall()
    for row in result:
        print(row)
        print("\n")


def create_customer(cursor, connection):
    """
    Function that creates a new customer.
    """
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
    elif len(pno) != 10:
        while len(pno) != 10:
            print("Enter 10 digit phone number.")
            pno = input("Enter customer phone number:\n")
    email = input("Enter customer email:\n")
    while "@" not in email:
        print("Enter valid email.")
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
    """
    Function that creates a new item.
    """
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
    """
    Function which searches for items on the basis of either name or type columns.
    """

    if identifier not in ("name, type"):
        # Error, this should not happen.
        return

    cursor.execute(
        "SELECT * FROM ITEMS WHERE {} LIKE '%{}%';".format(identifier, item_name)
    )

    result = cursor.fetchall()

    for row in result:

        stock = "In stock"

        if int(row[3]) <= 0:
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


def buy_item(item_number, cursor, connection):
    """
    Function which handles the purchase of an item by a customer.
    """
    query = "SELECT * FROM ITEMS WHERE INO = {}".format(item_number)
    cursor.execute(query)
    result = cursor.fetchone()
    cost = int(result[2])
    name = result[1]
    print("Name: ", name)
    print("Cost: ", cost)
    print("Type: ", result[4])

    confirmation = input("Please confirm if this is the product you want to buy:\n (Y)")
    if confirmation.lower() not in ("yes", "y"):
        return

    stock = int(result[3])
    if not stock:
        print("Item is not in stock. Please try again later.")
        return

    quantity = int(input("Please enter the quantity you want to purchase:\n"))

    while quantity > stock:
        print("Stock is only {}. Enter less quantity.".format(stock))
        quantity = int(input("Please enter the quantity you want to purchase:\n"))

    customer_number = int(input("Enter customer number:\n"))
    cursor.execute(
        "SELECT BALANCE, PASSWORD FROM CUSTOMERS WHERE CNO = {};".format(
            customer_number
        )
    )
    result = cursor.fetchone()
    balance = int(result[0])
    actual_password = result[1]
    if balance < quantity * cost:
        print("Insufficient balance.")
        return
    entered_password = input("Enter customer password:\n")
    if entered_password != actual_password:
        print("Wrong password.")
        return
    amount = quantity * cost
    today = str(date.today())
    print("-" * 25)
    print("Receipt".center(25))
    print("E-commerce project".center(25))
    print("Date: " + today)
    print("Customer number: {}".format(customer_number))
    print("Item: {}".format(name))
    print("Cost: {}".format(cost))
    print("Quantity: {}".format(quantity))
    print("-" * 25)
    print("Amount: {}".format(amount))
    print("-" * 25)
    input("Press enter to continue...")
    l = [customer_number, item_number, quantity, today]
    add_to_file(l)
    stock -= quantity
    new_balance = balance - amount
    cursor.execute(
        "UPDATE ITEMS SET STOCK = {} WHERE INO = {};".format(stock, item_number)
    )
    cursor.execute(
        "UPDATE CUSTOMERS SET BALANCE = {} WHERE CNO = {};".format(
            new_balance, customer_number
        )
    )
    connection.commit()
    print("Purchased successfully!")


def view_customer_details(customer_number, cursor):
    """
    Function to print customer details for admin.
    """
    cursor.execute("SELECT * FROM CUSTOMERS WHERE CNO={};".format(customer_number))
    result = cursor.fetchone()
    print("Name: ", result[1])
    print("Address: ", result[2])
    print("Phone number: ", result[3])
    print("E-mail: ", result[4])


def add_balance(bal, customer_number, cursor, connection):
    """
    Function to add balance in any given customer's account.
    """
    new = 0
    query = cursor.execute(
        "SELECT BALANCE FROM CUSTOMERS WHERE CNO={};".format(customer_number)
    )
    cursor.execute(query)
    result = cursor.fetchone()
    new = int(result[0]) + bal
    query1 = "UPDATE CUSTOMERS SET BALANCE = {} WHERE CNO={};".format(
        new, customer_number
    )
    cursor.execute(query1)
    connection.commit()


def edit_customer_details(customer_number, cursor):
    """
    Function to edit any customer's details.
    """
    new = 0
    # To print details of customer whose details are to be edited
    view_customer_details(customer_number, cursor)
    ch = "y"
    while ch.lower() == "y":
        print("\n 1.Name\n 2.Address\n 3.Phone Number:\n 4. E-mail\n")
        x = int(input("Enter detail to be edited:"))
        if x == 1:
            new = input("Enter new name:\n")
            cursor.execute(
                "UPDATE CUSTOMERS SET NAME='{}' WHERE CNO={};".format(
                    new, customer_number
                )
            )
        elif x == 2:
            new = input("Enter new address:\n")
            cursor.execute(
                "UPDATE CUSTOMERS SET ADDRESS='{}' WHERE CNO={};".format(
                    new, customer_number
                )
            )
        elif x == 3:
            new = input("Enter new phone number:\n")
            cursor.execute(
                "UPDATE CUSTOMERS SET PNO='{}' WHERE CNO={};".format(
                    new, customer_number
                )
            )

        elif x == 4:
            new = input("Enter new email:\n")
            cursor.execute(
                "UPDATE CUSTOMERS SET EMAIL='{}' WHERE CNO={};".format(
                    new, customer_number
                )
            )

        else:
            print("Incorrect choice")
        ch = input("Do you want to edit more details?(y/n)")


def add_stock(stock, item_number, cursor, connection):
    cursor.execute("SELECT STOCK FROM ITEMS WHERE INO={};".format(item_number))
    old_stock = cursor.fetchone()[0]
    new_stock = stock + old_stock
    cursor.execute(
        "UPDATE ITEMS SET STOCK={stock} WHERE INO={item};".format(
            stock=new_stock, item=item_number
        )
    )
    connection.commit()
    print("Added successfully. New stock is {}.".format(new_stock))
