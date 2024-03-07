import socket
import time

class Server:
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
    PORT_CLIENT = 65431
    cont = 0 
    isConnectedToClient = False 
    
    def send_to_client_response(self, ip, port, cont): 
        try:    
            if self.isConnectedToClient == False:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
                client_socket.connect((ip, port))         
            
            client_socket.sendall(bytes("bye "+str(cont), "utf-8"))
        except:
            return


    def start (self, on_received):
        s_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_in.bind((self.HOST, self.PORT))
        s_in.listen()
        print("Streaming server started...")
        conn, addr = s_in.accept()
        print(f"Connected by {addr[0]}") 
        
        while True:
            data = conn.recvfrom(1024)  
            if data and len(data)>0: 
                   
                on_received(data)
                
                # print(data)
                # time.sleep(2)
                # self.send_to_client_response(addr[0],self.PORT_CLIENT,self.cont)
                

       
                
                
                
  

