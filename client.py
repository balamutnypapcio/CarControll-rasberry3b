import socket
import threading

SERVER_IP = '10.112.3.4'  # IP serwera Raspberry Pi
PORT = 12000
# = "/home/kasper/soft/test.txt"
def send_messages(client):
    while True:
        try:
            with open("test", "a") as file:
                for line in file:
                    client_socket.sendall(line.encode())
                    print("Dane zostały wysłane")
            #message = client.recv(1024).decode()
            #print(f"\n{message}")
        except:
            print("Serwer zakonczyl prace")
            break
        finally:
            file.close()
            client.close()
            
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, 12000))
threading.Thread(target=send_messages, args=(client,), daemon=True).start()

#try:
 #   while True:
  #      message = input("Wpisz wiadomość (lub 'exit' aby zakończyć): ")
   #     if message.lower() == 'exit':
    #        break
     #   if message.lower() == '':
      #      break
       # client.send(message.encode())
        #response = client.recv(1024).decode()
        #print(f"[Serwer] {response}")
#finally:
 #   client.close()
