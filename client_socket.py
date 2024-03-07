import socket
import threading
import time


class Client:
    HOST = "127.0.0.1"  
    PORT_SEND = 65432  
    PORT_RECEIVED = 65431  
    s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          

        
    def send(self, data): 
        print("sending...")   
        self.s_out.sendall(data)
        

    def receive(self):        
        self.s_in.bind((self.HOST, self.PORT_RECEIVED))
        self.s_in.listen()        
        while True:
            conn, _ = self.s_in.accept()
            data = conn.recvfrom(1024)
            if data:
                print(data)
                time.sleep(2)
        
    
    def start(self):        
        self.s_out.connect((self.HOST, self.PORT_SEND))
        threadRecv = threading.Thread(target=self.receive)
        threadRecv.start()
   
            
        


