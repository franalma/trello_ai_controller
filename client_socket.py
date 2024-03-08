import socket
import threading
import time


class Client:
    
    # HOST = "101.46.143.21"
    # HOST = "192.168.2.126"  
    HOST = "192.168.2.31"  
    # LOCALHOST = "127.0.0.1"
    # HOST = "127.0.0.1"  
    PORT_SEND = 65432  
    PORT_RECEIVED = 65431  
    s_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    s_out.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)
    
    
    s_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)          

        
    def send(self, data): 
        # print(f"sending...{len(data)}")   
        self.s_out.sendall(data)
        # time.sleep(1)
      
        

    def receive(self):        
        self.s_in.bind((self.LOCALHOST, self.PORT_RECEIVED))
        self.s_in.listen()        
        while True:
            conn, _ = self.s_in.accept()
            data = conn.recvfrom(1024)
            if data:
                print(data)
                time.sleep(2)
                
    def receive2(self):                
        while True:
            data, _ = self.s_out.recvfrom(1024)
            print(data.decode("utf-8"))
            
        
    
    def start(self):        
        self.s_out.connect((self.HOST, self.PORT_SEND))            
        threadRecv = threading.Thread(target=self.receive2)
        threadRecv.start()
   
            
        


