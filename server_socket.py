import socket
import time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
PORT_CLIENT = 65431
cont = 0 
isConnectedToClient = False

def send_to_client_response(ip, port, cont): 
    try:    
        if isConnectedToClient == False:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
            client_socket.connect((ip, port))         
        
        client_socket.sendall(bytes("bye "+str(cont), "utf-8"))
    except:
        return


s_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s_in.bind((HOST, PORT))
s_in.listen()
conn, addr = s_in.accept()
while True:
    
   
    data = conn.recvfrom(1024)
    print (len(data))
    if data and len(data)>0: 
        print(f"Connected by {addr[0]}")    
        cont = cont +1
        data = []
        time.sleep(2)
        send_to_client_response(addr[0],PORT_CLIENT,cont)
        conn.

       
                
                
                
  

