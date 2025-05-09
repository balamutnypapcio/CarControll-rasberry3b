import socket
import threading
from datetime import datetime

HOST = '10.112.3.4'
PORT = 12000
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(2)

def handle_client(client_socket, address):
    print(f"Połączono z {address}")
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            
            # Dekodowanie otrzymanych danych
            message = data.decode("utf-8")
            
            # Dodanie znacznika czasu
            timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            
            # Zapisanie danych do pliku
            with open("input_data.txt", "a") as file:
                # Formatowanie linii z timestampem i adresem klienta
                log_line = f"[{timestamp}] {address} - {message}"
                file.write(log_line)
                print(f"Zapisano: {log_line.strip()}")
                
        except ConnectionResetError:
            break
        except Exception as e:
            print(f"Błąd: {e}")
            break
            
    print(f"[Info] Rozłączono z {address}")
    if client_socket in clients:
        clients.remove(client_socket)
    client_socket.close()

print(f"[INFO] Serwer nasłuchuje na porcie {PORT}...")

while True:
    try:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()
    except Exception as e:
        print(f"Błąd podczas akceptowania połączenia: {e}")
