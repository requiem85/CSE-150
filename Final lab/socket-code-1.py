import argparse
from socket import *
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

try:
#    server_ip, server_port = args.server.split(":")
    server_port = args.port #server port
    server_ip = args.server #server ip
except ValueError:
   print("Invalid server argument. Format: IP:Port")
   exit(1)

s = socket(AF_INET, SOCK_STREAM)
print(server_ip, int(server_port))
s.connect((server_ip, server_port))
# Main loop
while True:
   user_input = input("Enter command: ").lower()
   print(user_input)

   if user_input == "/id":
       print("Your ID:", args.id)

   elif user_input == "/register":
    #    with socket(AF_INET, SOCK_STREAM) as s:
        #    s.bind(("127.0.0.1", server_port))
        #    s.listen(1)
        #    s.settimeout(5)
           print(server_ip, int(server_port))
        #    s.connect((server_ip, int(server_port)))
           sys.stdout.write("yo yo you")
           s.sendall("REGISTER\r\nclientID: {}\r\nIP: {}\r\nPort: {}\r\n".format(args.id,server_ip, server_port).encode("utf-8")[:1024])

           response = s.recv(1024).decode("utf-8")
        #    mininet]
   elif user_input == "/bridge":
       with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
           s.connect((server_ip, int(server_port)))
           s.sendall(f"/bridge {args.id}".encode())
           response = s.recv(1024).decode()
           # Process the bridge response here
           print("Bridge response:", response)

   elif user_input == "/exit":
       break

   else:
       print("Invalid command.")

print("Program terminated.")
