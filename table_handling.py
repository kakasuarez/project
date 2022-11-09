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

    cursor.execute(
        "INSERT INTO CUSTOMERS VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(
            customer_number, name, address, pno, email, password
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
