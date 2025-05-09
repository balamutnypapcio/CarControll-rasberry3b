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
    "gas": 0,       # 0-100
    "brake": 0,     # 0-100
    "gear": "0"     # 0, 1, 2, 3, 4, 5, R
}

def send_message(client, message):
    try:
        client.sendall(message.encode())
        print(f"Wysłano: {message}")
    except:
        print("Błąd wysyłania danych do serwera")

def main():
    global state
    
    # Połączenie z serwerem
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_IP, PORT))
    except:
        print("Nie można połączyć się z serwerem")
        return

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                message = ""
                if event.key == pygame.K_UP:
                    state["gas"] = min(state["gas"] + 20, 100)  # Zwiększenie gazu
                    message = f"Gas: {state['gas']}\n"
                elif event.key == pygame.K_DOWN:
                    state["brake"] = min(state["brake"] + 20, 100)  # Zwiększenie hamulca
                    message = f"Brake: {state['brake']}\n"
                elif event.key == pygame.K_0:
                    state["gear"] = "0"
                    message = f"Gear: {state['gear']}\n"
                elif event.key == pygame.K_1:
                    state["gear"] = "1"
                    message = f"Gear: {state['gear']}\n"
                elif event.key == pygame.K_2:
                    state["gear"] = "2"
                    message = f"Gear: {state['gear']}\n"
                elif event.key == pygame.K_3:
                    state["gear"] = "3"
                    message = f"Gear: {state['gear']}\n"
                elif event.key == pygame.K_4:
                    state["gear"] = "4"
                    message = f"Gear: {state['gear']}\n"
                elif event.key == pygame.K_5:
                    state["gear"] = "5"
                    message = f"Gear: {state['gear']}\n"
                elif event.key == pygame.K_r:
                    state["gear"] = "R"
                    message = f"Gear: {state['gear']}\n"
                
                if message:
                    send_message(client, message)
            
            elif event.type == pygame.KEYUP:
                message = ""
                if event.key == pygame.K_UP:
                    state["gas"] = max(state["gas"] - 20, 0)  # Zmniejszenie gazu po puszczeniu
                    message = f"Gas: {state['gas']}\n"
                elif event.key == pygame.K_DOWN:
                    state["brake"] = max(state["brake"] - 20, 0)  # Zmniejszenie hamulca po puszczeniu
                    message = f"Brake: {state['brake']}\n"
                
                if message:
                    send_message(client, message)

    client.close()
    pygame.quit()

if __name__ == "__main__":
    main()
