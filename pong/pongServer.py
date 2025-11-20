# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

clients = []

# =================================================================================================
# Author: <Who wrote this method> 
# Purpose: <What should this method do>
# Pre: <What preconditions does this method expect to be true? Ex. This method expects the program to be in X state before being called> 
# Post: <What postconditions are true after this method is called? Ex. This method changed global variable X to Y>
# =================================================================================================
def handle_clients(conn: socket.socket, addr: tuple) -> None:

    # initial width and height to the client
    conn.send(b"640,480")

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

        conn.close()
        if conn in clients:
            clients.remove(conn)
    
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(("127.0.0.1", 12345))
server.listen()

print("Listening on port 12345...")

while True:
    conn, addr= server.accept()
    clients.append(conn)
    thread = threading.Thread(target=handle_clients, args=(conn, addr), daemon=True)
    thread.start()
