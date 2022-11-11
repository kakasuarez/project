password_file = "pass.bin"
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

    return True


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