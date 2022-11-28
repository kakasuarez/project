"""
File which deals with all the functions for manipulating and storing the passwords.
There are two passwords to be stored:
First is the database password for MySQL.
Second is the admin password.
The passwords are stored in the binary file named pass.bin.
"""


# The name of the password file.
password_file = "pass.bin"

# Maximum length of both passwords.
max_size_of_pass = 30


def write_password(password):
    """
    Writes a given password to the binary file. The given password should either be the database password (MySQL) or admin password.
    It is assumed that database password will be writen first.
    """
    length = len(password)

    if length > max_size_of_pass:
        return

    password += (max_size_of_pass - length) * " "
    password = password.encode()

    with open(password_file, "ab") as f:
        f.write(password)


def read_password(type):
    """
    Reads the password of the requested type from the file and returns it. Type should either be 1 for MySQL or 2 for admin.
    """
    if type not in (1, 2):
        return

    position = max_size_of_pass * (type - 1)

    with open(password_file, "rb") as f:
        f.seek(position)
        password = f.read(max_size_of_pass)
        password = password.decode()

    password = password.rstrip()
    return password


def ask_for_admin():
    """
    Function which logs in the user as admin.
    """
    admin_password = input("Enter admin password:\n")

    saved_password = read_password(2)
    if admin_password == saved_password:
        print("Logged in as admin successfully.")
        return True
    else:
        print("Wrong password.")
        return False
