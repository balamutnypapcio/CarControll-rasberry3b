import socket
import pygame
import time

SERVER_IP = '10.112.3.4'  # IP serwera Raspberry Pi
PORT = 12000

# Inicjalizacja Pygame do obsługi klawiatury
pygame.init()
screen = pygame.display.set_mode((200, 200))  # Minimalne okno, nieużywane do wyświetlania
pygame.display.set_caption("Car Client")

# Stan samochodu
state = {
    "gaz": 0,       # 0-100
    "hamulec": 0,   # 0-100
    "bieg": "0"     # 0, 1, 2, 3, 4, 5, R
}

# Zmienne do śledzenia czasu trzymania klawiszy
gaz_start_time = None
hamulec_start_time = None

def send_message(client, message):
    try:
        client.sendall(message.encode())
        print(f"Wysłano: {message}")
    except:
        print("Błąd wysyłania danych do serwera")

def update_value(current_value, start_time):
    if start_time is not None:
        elapsed_time = time.time() - start_time
        new_value = min(current_value + elapsed_time * 5, 100)  # 5 jednostek na sekundę
        return new_value
    return current_value

def main():
    global state, gaz_start_time, hamulec_start_time
    
    # Połączenie z serwerem
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_IP, PORT))
    except:
        print("Nie można połączyć się z serwerem")
        return

    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                message = ""
                if event.key == pygame.K_UP:
                    gaz_start_time = time.time()  # Rozpoczęcie trzymania gazu
                elif event.key == pygame.K_DOWN:
                    hamulec_start_time = time.time()  # Rozpoczęcie trzymania hamulca
                elif event.key == pygame.K_0:
                    state["bieg"] = "0"
                    message = f"Bieg: {state['bieg']}\n"
                elif event.key == pygame.K_1:
                    state["bieg"] = "1"
                    message = f"Bieg: {state['bieg']}\n"
                elif event.key == pygame.K_2:
                    state["bieg"] = "2"
                    message = f"Bieg: {state['bieg']}\n"
                elif event.key == pygame.K_3:
                    state["bieg"] = "3"
                    message = f"Bieg: {state['bieg']}\n"
                elif event.key == pygame.K_4:
                    state["bieg"] = "4"
                    message = f"Bieg: {state['bieg']}\n"
                elif event.key == pygame.K_5:
                    state["bieg"] = "5"
                    message = f"Bieg: {state['bieg']}\n"
                elif event.key == pygame.K_r:
                    state["bieg"] = "R"
                    message = f"Bieg: {state['bieg']}\n"
                
                if message:
                    send_message(client, message)
            
            elif event.type == pygame.KEYUP:
                message = ""
                if event.key == pygame.K_UP:
                    gaz_start_time = None  # Zatrzymanie liczenia gazu
                    message = f"Gaz: {state['gaz']}\n"
                elif event.key == pygame.K_DOWN:
                    hamulec_start_time = None  # Zatrzymanie liczenia hamulca
                    message = f"Hamulec: {state['hamulec']}\n"
                
                if message:
                    send_message(client, message)

        # Aktualizacja wartości gazu i hamulca w czasie rzeczywistym
        previous_gaz = state["gaz"]
        previous_hamulec = state["hamulec"]
        
        state["gaz"] = update_value(state["gaz"], gaz_start_time)
        state["hamulec"] = update_value(state["hamulec"], hamulec_start_time)
        
        # Wysłanie aktualizacji, jeśli wartości się zmieniły
        if state["gaz"] != previous_gaz:
            send_message(client, f"Gaz: {state['gaz']}\n")
        if state["hamulec"] != previous_hamulec:
            send_message(client, f"Hamulec: {state['hamulec']}\n")

        clock.tick(60)  # Ograniczenie do 60 FPS dla płynności

    client.close()
    pygame.quit()

if __name__ == "__.Tags:
- Python
- Raspberry Pi
- Pygame
- Socket Programming
- Client-Server
- Real-time Input
