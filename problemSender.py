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

        current_slope = 0
        slope_duration = 0
        slope_time_left = 0

        while True:
            # Szansa na przeszkodę: 10%
            przeszkoda = 1 if random.random() < 0.1 else 0

            # Obsługa nachylenia
            if slope_time_left <= 0:
                if random.choice([True, False]):  # Czy ma być nachylenie?
                    # Losuj nachylenie od -30 do 30, pomijając 0
                    current_slope = random.choice([i for i in range(-30, 31) if i != 0])
                    slope_duration = random.randint(1, 10)
                    slope_time_left = slope_duration
                else:
                    current_slope = 0
                    slope_time_left = random.randint(1, 10)

            nachylenie = current_slope
            slope_time_left -= 1

            # Tworzenie wiadomości i wysyłanie
            message = f"[slope {nachylenie},barrier {przeszkoda}]"
            client.send(message.encode())
            print(f"Wysłano: {message}")

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
