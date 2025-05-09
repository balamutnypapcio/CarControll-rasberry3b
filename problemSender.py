import socket
import time
import random

SERVER_IP = '10.112.3.4'
PORT = 12000

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_IP, PORT))
        print(f"Połączono z serwerem {SERVER_IP}:{PORT}")

        while True:
            # Generowanie losowych danych
            nachylenie = random.randint(0, 100)
            przeszkoda = random.randint(0, 1)
            
            # Tworzenie wiadomości i wysyłanie
            message = f"[{nachylenie},{przeszkoda}]"
            client.send(message.encode())
            
            # Czekaj 1 sekundę przed następnym wysłaniem
            time.sleep(1)

    except ConnectionRefusedError:
        print("Nie można połączyć się z serwerem")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
