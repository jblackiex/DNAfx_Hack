import socket

HOST = '0.0.0.0'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Riutilizza la porta anche se è in TIME_WAIT
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected by {addr}")
        
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"Connection closed by {addr}")
                break
            print(f"Received from {addr}: {data.decode()}")
        
        client_socket.close()

except OSError as e:
    print(f"Error binding to port {PORT}: {e}")

finally:
    server_socket.close()

