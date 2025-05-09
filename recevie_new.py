import socket
import threading

HOST = '10.112.3.4'
PORT = 12000
clients = []
lock = threading.Lock()  # Lock dla bezpiecznego dostępu do listy clients

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(2)

def handle_client(client_socket, address):
    print(f"Połączono z {address}")
    while True:
        try:
            data = client_socket.recv(1024)  # Odbieranie danych od klienta
            if not data:
                break
            with lock:
                with open("input_data.txt", "a") as file:
                    file.write(data.decode("utf-8"))
                    file.flush()
            print(f"Odebrano od {address}: {data.decode('utf-8').strip()}")
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            break
        except Exception as e:
            print(f"Błąd podczas obsługi klienta {address}: {e}")
            break
    
    print(f"[Info] Rozłączono z {address}")
    with lock:
        if client_socket in clients:
            clients.remove(client_socket)
    client_socket.close()

def main():
    print(f"Serwer uruchomiony na {HOST}:{PORT}")
    while True:
        try:
            client_socket, addr = server.accept()
            with lock:
                clients.append(client_socket)
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()
        except Exception as e:
            print(f"Błąd podczas akceptowania połączenia: {e}")
            break

    server.close()

if __name__ == "__main__":
    main()
