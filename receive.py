import socket
import threading

HOST = '10.112.3.4'
PORT = '12000'
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server.bind((HOST, 12000))
server.listen(2)

def handle_client(client_socket, address):
	print(f"Połączono z {address}")
	while True:
		try:
			conn, addr = server.accept()
			data = conn.recv(1024)
			if not data:
				break
			file = open("input_data.txt", "a")
			file.write(data.decode("utf-8"))
			file.flush()
			file.close()
		except ConnectionResetError:
			break
	print(f"[Info] Rozłączono z {address}")
	clients.remove(client_socket)
	client_socket.close()

while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
