import socket
import threading
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT_SEND = 65432  # The port used by the server
PORT_RECEIVED = 65431  # The port used by the server

s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s_out.connect((HOST, PORT_SEND))


                
def send_host(data): 
    print("sending...")   
    s_out.sendall(data)
        

def receive():
    s_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          
    s_in.bind((HOST, PORT_RECEIVED))
    s_in.listen()        
    
    
    while True:
        conn, _ = s_in.accept()
        data = conn.recvfrom(1024)
        if data:
            print(data)
            time.sleep(2)
       
threadRecv = threading.Thread(target=receive)
threadRecv.start()
 
while True:
    time.sleep(2)
   
    send_host(b"Hi")
   
            
        


