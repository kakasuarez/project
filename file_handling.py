"""
File which deals with all the procedures related to the csv file, orders.csv.
The csv file contains the records of all the transactions that have occured.
"""


import csv
import os
from datetime import datetime

# Header of the csv file.
header = ["customer number", "item number", "quantity", "date"]

# Orders file name.
orders_file = "orders.csv"


def get_rate(item_no, cursor):
    cursor.execute("SELECT COST FROM ITEMS WHERE INO={};".format(item_no))
    result = cursor.fetchone()
    result = result[0]
    return result


def create_file():
    """
    Function that creates the csv if it does not exist.
    """

    # To check if the file already exists.
    if os.path.exists(orders_file):
        return

    # Create the file if it doesn't exist.
    file = open(orders_file, "w+", newline="")
    writer = csv.writer(file)
    writer.writerow(header)
    file.close()


def add_to_file(li):
    """
    Function that adds a record of a new order to the csv file.
    """
    file = open(orders_file, "a", newline="")
    writer = csv.writer(file)
    writer.writerow(li)
    file.close()


def get_revenue(row, cursor):
    item_no = int(row[1])
    quantity = int(row[2])
    rate = get_rate(item_no, cursor)
    revenue = rate * quantity
    return revenue


def read_file(cursor):
    """
    Function that prints all the orders recorded in the csv file.
    """
    file = open(orders_file, "r")
    reader = csv.reader(file, delimiter=",")
    # To skip header line.
    next(reader)
    for row in reader:
        print("=" * 50)
        print()
        for i in range(len(row)):
            print(header[i] + ": " + row[i])
        revenue = get_revenue(row, cursor)
        print("Revenue:" + str(revenue))


def get_monthly_revenue(cursor):
    """
    Function that prints the report of each month.
    """
    file = open(orders_file, "r")
    reader = csv.reader(file, delimiter=",")
    # To skip header line.
    next(reader)
    first_order = next(reader)
    first_month = datetime.strptime(first_order[3], "%Y-%m-%d").date().month
    revenue = get_revenue(first_order, cursor)
    for row in reader:
        d = datetime.strptime(row[3], "%Y-%m-%d").date().month
        if d == first_month:
            revenue += get_revenue(row, cursor)
        else:
            print(f"Revenue of {first_month} month:" + str(revenue))
            first_month = d
            revenue = get_revenue(row, cursor)
    print(f"Revenue of {first_month} month:" + str(revenue))
