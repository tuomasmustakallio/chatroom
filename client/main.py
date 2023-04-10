import socket
import threading

ADDRESS = "127.0.0.1"
PORT = 8000

## Function that handles the receiving of messages and prints them to the console
def receive_message(client):
     while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if(message):
                print(message)
        except:
            print("Error, connection lost")
            client.close()
            break

def main():

    ## Create a socket and connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ADDRESS, PORT))

    ## Get the username and channel from the user
    username = input("Enter your username: ")
    channel = input("Enter the channel you want to join: ")

    ## Send the username and channel to the server
    client.sendall(f"{username}\n{channel}".encode('utf-8'))
    ## Start a thread that handles the receiving of messages
    threading.Thread(target=receive_message, args=(client,)).start()

    print ("Type /quit to exit")

    while True:
        message = input()
        
        if message == "/quit":
            client.sendall("DISCONNECT".encode('utf-8'))
            client.close()
            break
        else:
            ## Send the message to the server
            client.sendall(f"{message}\n".encode('utf-8'))

if __name__ == '__main__':
    main()