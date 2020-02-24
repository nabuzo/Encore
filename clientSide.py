# Authors: Jaelyn Fladger, Nicole Abuzo, Kodie Philips, Joseph Ankebrant, Alejandro Huerta
# Date: November 11, 2019
# Description: A ticket purchasing program name Encore. Simple program that is vulnerable from attacks.


import socket


print(" __    __    ___  _        __   ___   ___ ___    ___      ______   ___         ___  ____     __   ___   ____     ___ ")
print("|  |__|  |  /  _]| |      /  ] /   \ |   |   |  /  _]    |      | /   \       /  _]|    \   /  ] /   \ |    \   /  _]")
print("|  |  |  | /  [_ | |     /  / |     || _   _ | /  [_     |      ||     |     /  [_ |  _  | /  / |     ||  D  ) /  [_ ")
print("|  |  |  ||    _]| |___ /  /  |  O  ||  \_/  ||    _]    |_|  |_||  O  |    |    _]|  |  |/  /  |  O  ||    / |    _]")
print("|  `  '  ||   [_ |     /   \_ |     ||   |   ||   [_       |  |  |     |    |   [_ |  |  /   \_ |     ||    \ |   [_ ")
print(" \      / |     ||     \     ||     ||   |   ||     |      |  |  |     |    |     ||  |  \     ||     ||  .  \|     |")
print("  \_/\_/  |_____||_____|\____| \___/ |___|___||_____|      |__|   \___/     |_____||__|__|\____| \___/ |__|\_||_____|")
                                                                                                                     


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening

server_address = ('localhost', 10001)
sock.connect(server_address)


serverMessage = sock.recv(1024)

while serverMessage.decode() != "close":
    serverMessage = sock.recv(4000)

    if serverMessage.decode() == "respond":
        while True:
            response = input(">>> ")
            if (len(response) > 50):
                print ("Your response is to large.")
            else:
                sock.sendall(response.encode())
                break
    else:
        print(serverMessage.decode())
        

sock.close()
