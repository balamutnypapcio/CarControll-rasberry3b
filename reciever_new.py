import socket
import threading

HOST = '10.112.3.4'
PORT = 12000
clients = []

# Zmienne do przechowywania stanu
car_state = {
    "gas": 0,
    "brake": 0,
    "gear": "0"
}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(2)

def update_car_state(message):
    """Aktualizuje stan samochodu na podstawie otrzymanej wiadomości"""
    try:
        key, value = message.split(": ")
        value = value.strip()  # Usuwa whitespace i znaki nowej linii
        
        if key == "Gas":
            car_state["gas"] = int(value)
        elif key == "Brake":
            car_state["brake"] = int(value)
        elif key == "Gear":
            car_state["gear"] = value
            
        print(f"Aktualny stan pojazdu: {car_state}")
    except Exception as e:
        print(f"Błąd podczas przetwarzania wiadomości: {e}")

def handle_client(client_socket, address):
    print(f"Połączono z {address}")
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
                
            # Dekodowanie i wyświetlenie wiadomości
            message = data.decode("utf-8")
            print(f"Otrzymano od {address}: {message.strip()}")
            update_car_state(message)
                
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
