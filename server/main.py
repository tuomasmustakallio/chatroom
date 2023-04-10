import threading
import socket

ADDRESS = "127.0.0.1"
PORT = 8000

## Class that represents a channel and holds a dictionary of users
class Channel:
    def __init__(self, name):
        self.name = name
        self.users = {}

## Class that represents a client and holds the username, socket and channel
class Client:
    def __init__(self, username, sock, channel):
        self.username = username
        self.sock = sock
        self.channel = channel

## Dictionary that holds all the channels
channels = {}

## Function that handles the receiving of messages and prints them to the console
def handle_client(client):
    while True:
        try:
            ## Receive the message from the client
            message = client.sock.recv(1024).decode('utf-8').strip()
            ## If the message is DISCONNECT, close the socket and break the loop
            if message == 'DISCONNECT':
                client.sock.close()
                break
            ## If the message is not DISCONNECT, send the message to all the users in the channel
            else:
                print(client.channel.users)
                ## Loop through all the users in the channel and send the message to all of them
                for user in client.channel.users:
                    if user != client.username:
                        client.channel.users[user].sock.send(f"{client.username}: {message}".encode('utf-8'))
        ## If an error occurs, close the socket and break the loop
        except Exception as e:
            print(e)
            client.sock.close()
            break

def main():
    ## Create a socket and bind it to the address and port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ADDRESS, PORT))
    server.listen()
    print('Listening on port', PORT)
    while True:
        ## Accept a connection and get the client socket and address
        client_sock, client_address = server.accept()
        print('Connected to', client_address)

        ## Receive the username and channel from the client
        message = client_sock.recv(1024).decode('utf-8').split('\n')
        
        ## Create a client and a channel if they don't exist
        client_name = message[0]
        if message[1] not in channels:
            channels[message[1]] = Channel(message[1])
        client_channel = channels[message[1]]
        client = Client(client_name, client_sock, client_channel)
        if client.username not in channels[message[1]].users:
            channels[message[1]].users[client.username] = client
        
        ## Start a thread that handles the receiving of messages
        threading.Thread(target=handle_client, args=(client,)).start()
        print(f'Client {client_name} connected to the server!')

        ## Send a message to the client that they have connected to the channel
        client.sock.send(f"You have connected to {client.channel}!\n".encode('utf-8'))

if __name__ == '__main__':
    main()