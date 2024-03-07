import argparse
import socket
import sys

# Parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument("--id", type=str, required=True, help="Client ID")
parser.add_argument("--port", type=int, required=True, help="Client port")
parser.add_argument("--server", type=str, required=True, help="Server IP:Port number")
args = parser.parse_args()

# Validate port and server arguments
if not 1024 <= args.port <= 65535:
    print("Invalid port number. Must be between 1024 and 65535.")
    exit(1)

port = args.port

try:
    server_ip, server_port = args.server.split(":")
    # server_port = args.port #server port
    # server_ip = args.server #server ip
except ValueError:
    print("Invalid server argument. Format: IP:Port")
    exit(1)

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

valid = ["/id", "/register", "/bridge", "/chat", "/quit"]

print(server_ip, int(server_port))

peer_ip = None
peer_port = None

# Main loop
while True:
    user_input = input("Enter command: ").lower()
    print(user_input)
    if user_input not in valid:
        print("Invalid command.")
        continue
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        if user_input == "/id":
            print("Your ID:", args.id)

        elif user_input == "/register":
            s.connect((server_ip, int(server_port)))
            #    with socket(AF_INET, SOCK_STREAM) as s:
            #    s.bind(("127.0.0.1", server_port))
            #    s.listen(1)
            #    s.settimeout(5)
            #   server_ip, server_port = args.server.split(":")
            #   print(server_ip, int(server_port))
            #    s.connect((server_ip, int(server_port)))
            # sys.stdout.write("yo yo you")
            # print("test1")
            data = (
                "REGISTER\r\n"
                + "clientID: {}\r\n".format(args.id)
                + "IP: {}\r\n".format(server_ip)
                + "Port: {}\r\n".format(port)
                + "\r\n"
            )
            # print(data)
            s.send(data.encode())
            # print("test2")
            response = s.recv(1024)
            print("Register response:", response.decode())
        #    s.close()
        #    mininet]
            s.close()
        elif user_input == "/bridge":
            s.connect((server_ip, int(server_port)))
            #    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            data = "BRIDGE\r\nclientID: {}\r\n\r\n".format(args.id)
            # s.connect((server_ip, int(server_port)))
            # print(data2)
            s.send(data.encode())
            response = s.recv(1024).decode()
            # Process the bridge response here
            print("Bridge response:", response)
            response = response.split("\r\n")
            peer_id = response[1].split(": ")[1]
            peer_ip = response[2].split(": ")[1]
            peer_port = response[3].split(": ")[1]

            if peer_id and peer_ip and peer_port:
                print("Peer found:", peer_id, peer_ip, peer_port)
                peer_port = int(peer_port)
            else:
                # first client, wait for peer to start connection, then send data back
                print("No peer found.")
                s.close()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(('', port))
                s.listen(1)
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(1024).decode()
                        if data == "QUIT\r\n\r\n":
                            exit(0)
                        print(data)
                        i = input()
                        if i == "/quit":
                            conn.sendall("QUIT\r\n\r\n".encode())
                            exit(0)
                        conn.sendall(i.encode())

            s.close()
        elif user_input == "/chat":
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((peer_ip, peer_port))
            while True:
                i = input()
                if i == "/quit":
                    s.sendall("QUIT\r\n\r\n".encode())
                    break
                s.sendall(i.encode())
                data = s.recv(1024).decode()
                if data == "QUIT\r\n\r\n":
                    exit(0)
                print(data)
            s.close()


print("Program terminated.")
