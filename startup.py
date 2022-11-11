import mysql.connector as mysql
import os
from password_handling import (
    password_file,
    read_password,
    max_size_of_pass,
    write_password,
)


def create_admin_account():
    """
    Creates an admin account.
    """
    admin_password = input(
        "Enter admin password (maximum %s characters):\n" % max_size_of_pass
    )
    write_password(admin_password)


def connect():
    """
    Function to connect to the database and store the password.
    """

    if os.path.exists(password_file):
        password = read_password(1)

    else:
        print("Saved password not found.")
        password = input(
            "Enter database password (maximum %s characters):\n" % max_size_of_pass
        )
        write_password(password)

        create_admin_account()

    connection = mysql.connect(host="localhost", user="root", password=password)

    if connection.is_connected():
        print("Connected successfully!")

    return connection


def get_cursor(connection):
    """
    Returns cursor from a given connection.
    """
    return connection.cursor()


def create_tables(cursor):
    """
    Creates the required tables for the project.
    """
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS ITEMS (INO INT(5) PRIMARY KEY, NAME VARCHAR(20), COST INT(6), STOCK INT(3), TYPE VARCHAR(20));"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS CUSTOMERS (CNO INT(5) PRIMARY KEY, NAME VARCHAR(20) NOT NULL, ADDRESS VARCHAR(50) NOT NULL, PNO CHAR(10), EMAIL VARCHAR(30) UNIQUE, PASSWORD VARCHAR(50) NOT NULL, BALANCE INT(6) NOT NULL);"
    )


def create_database(cursor):
    """
    Creates the database for the project if it does not exist.
    """
    cursor.execute("CREATE DATABASE IF NOT EXISTS ECOM;")
    cursor.execute("USE ECOM;")
    create_tables(cursor)
