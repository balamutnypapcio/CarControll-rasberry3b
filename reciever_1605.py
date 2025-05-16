import socket
import threading
import json
import re

HOST = '10.112.3.4'
PORT = 12000

# Global variables to store the state
car_state = {
    "gaz": 0,
    "hamulec": 0,
    "bieg": "0"
}

environment_state = {
    "nachylenie": 0,
    "przeszkoda": 0
}

# Lock for thread-safe operations
state_lock = threading.Lock()

def parse_car_data(data):
    """Parse data from Client_1.py"""
    try:
        # Data format example: "Gaz: 50" or "Hamulec: 30" or "Bieg: 2"
        key, value = data.strip().split(': ')
        key = key.lower()
        if key in ['gaz', 'hamulec']:
            return key, float(value)
        elif key == 'bieg':
            return key, value
        return None, None
    except:
        return None, None

def parse_environment_data(data):
    """Parse data from problemSender.py"""
    try:
        # Data format example: "[30,1]"
        match = re.match(r'\[(-?\d+),(\d+)\]', data)
        if match:
            nachylenie = int(match.group(1))
            przeszkoda = int(match.group(2))
            return nachylenie, przeszkoda
        return None, None
    except:
        return None, None

def handle_client(client_socket, address):
    print(f"Połączono z {address}")
    
    while True:
        try:
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break
                
            # Try to parse as car control data
            key, value = parse_car_data(data)
            if key is not None:
                with state_lock:
                    car_state[key] = value
                print(f"Car State Updated: {car_state}")
                
            # Try to parse as environment data
            nachylenie, przeszkoda = parse_environment_data(data)
            if nachylenie is not None:
                with state_lock:
                    environment_state["nachylenie"] = nachylenie
                    environment_state["przeszkoda"] = przeszkoda
                print(f"Environment State Updated: {environment_state}")
            
            # Save to file
            with open("input_data.txt", "a") as file:
                timestamp = threading.current_thread().name
                file.write(f"[{timestamp}] {data}\n")
                
        except ConnectionResetError:
            break
            
    print(f"[Info] Rozłączono z {address}")
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(2)
    
    print(f"Serwer nasłuchuje na {HOST}:{PORT}")
    
    try:
        while True:
            client_socket, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.name = f"Client-{addr[0]}:{addr[1]}"
            client_thread.start()
    except KeyboardInterrupt:
        print("\nZamykanie serwera...")
    finally:
        server.close()

if __name__ == "__main__":
    main()
