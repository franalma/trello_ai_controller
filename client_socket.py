import socket
import threading
import time
import numpy as np


class Client:
    
    HOST = "101.46.143.21"
    # HOST = "192.168.2.126"  
    # HOST = "192.168.2.31"  
    # LOCALHOST = "127.0.0.1"
    # HOST = "127.0.0.1"  
    PORT_SEND = 65432  
    PORT_RECEIVED = 65431  
    s_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    s_out.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)
    listener:any
    
    s_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)          

    def calc_diff (self, data):    
        if (len(data)>30000):
                cosine = -1
                slice_data = data[:30000]     
                if len(self.prev_buffer)> 0:                   
                    cosine = np.dot(self.prev_buffer,slice_data)/(norm(self.prev_buffer)*norm(slice_data))
                    # print("cosine: "+str(cosine))
                self.prev_buffer = slice_data   
                if cosine < 7.0e-08 :  
                    print ("processing")    
        
    def send(self, data):         
        self.s_out.sendall(data)
        
    def send_with_listener(self, data, listener):         
        self.listener = listener
        # print(len(data))
        self.s_out.sendall(data) 
        

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
            if self.listener:
                self.listener(data.decode("utf-8"))
            
    def start(self):        
        self.s_out.connect((self.HOST, self.PORT_SEND))            
        threadRecv = threading.Thread(target=self.receive2)
        threadRecv.start()
   
            
        


