"""
File which deals with all the procedures related to the csv file, orders.csv.
The csv file contains the records of all the transactions that have occured.
"""


import csv
import os


# Header of the csv file.
header = ["customer number", "item number", "quantity", "date"]

# Orders file name.
orders_file = "orders.csv"


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


def read_file():
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
