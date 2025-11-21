# =================================================================================================
# Contributing Authors:	    Rowan Hallock, Ben Shuler, Nate Berry
# Email Addresses:          rha321@uky.edu, bmsh239@uky.edu, nbbe226@uky.edu
# Date:                     11/21/2025
# Purpose:                  This file handles the server logic for the pong game. It is responsible for handling the connections from the clients and sharing the data between them.
# Misc:                     N/A
# =================================================================================================

import socket
import threading
import time

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

clients = []

# =================================================================================================
# Author: Rowan Hallock, Ben Shuler, Nate Berry
# Purpose: Handles the communication between the clients and the server.
# Pre: The server is running and the clients are connected.
# Post: The data is shared between the clients and the server.
# =================================================================================================
def handle_clients(conn: socket.socket, addr: tuple) -> None:

    try:

        # wait for other player to connect
        while len(clients) < 2:
            time.sleep(0.5)

        # assign sides
        if clients.index(conn) == 0:
            side = "left"
        elif clients.index(conn) == 1:
            side = "right"
        else:
            side = "spectator"
        

        # initial width and height to the client
        msg = f"640,480,{side}"
        conn.send(msg.encode())

        # recieve the data from client
        while True: 
            try:
                data = conn.recv(1024)
                if not data:
                    break
                for c in clients:
                    if c != conn:
                        c.send(data)
            except:
                break
    finally:
        try:
            conn.close()
        finally:
            if conn in clients:
                clients.remove(conn)
    
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind to 0.0.0.0 to allow connection from external devices
server.bind(("0.0.0.0", 12345))
server.listen()

print("Listening on port 12345")

# listen for connection
while True:
    conn, addr = server.accept()
    clients.append(conn)
    thread = threading.Thread(target=handle_clients, args=(conn, addr), daemon=True)
    thread.start()
