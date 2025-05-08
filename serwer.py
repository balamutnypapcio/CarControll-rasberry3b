import socket
import threading

HOST = '10.112.3.32'
PORT = 12000
clients = []

def handle_client(client_socket, address):
    print(f"Połączono z {address}")
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"[{address}] Otrzymano {data}")
            client_socket.send(f"Serwer otrzymał: {data}".encode())
        except ConnectionResetError:
            break
    print(f"[Info] Rozłączono z {address}")
    clients.remove(client_socket)
    client_socket.close()
    
def send_to_clients():
    while True:
        message = input("Serwer: ")
        if message.lower() == 'exit':
            print("Zamykanie serwera")
            for client in clients:
                client.send("Serwer zakonczyl dzialanie".encode())
                client.close()
            exit()
        for client in clients:
            try:
                client.send(f"Serwer: {message}".encode())
            except:
                clients.remove(client)
            
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, 12000))
server.listen(2)

print(f"[INFO] Serwer nasłuchuje na {PORT}...")
threading.Thread(target=send_to_clients, daemon=True).start()

while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
        
