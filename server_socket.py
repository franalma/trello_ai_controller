import socket
import time
import numpy as np
from numpy.linalg import norm
import pickle,struct

class Server:
    # HOST = "192.168.2.31" 
    HOST = "0.0.0.0"
    PORT = 65432  
    PORT_CLIENT = 65431
    s_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    isConnectedToClient = False 
    prev_buffer =[]
    isDisplayEnabled = False
    
    def send_to_client_response(self, ip, port, command): 
        try:                            
            # client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                        
            # client_socket.sendto(bytes(command),(ip, port))        
            self.s_in.sendto(bytes(command,"utf-8"),(ip, port))
        except:
            return

    
    def calculate_frame_distance(self, data):
        cosine = -1
        slice_data = data[:30000]     
    
        if len(self.prev_buffer)> 0:                   
            cosine = np.dot(self.prev_buffer,slice_data)/(norm(self.prev_buffer)*norm(slice_data))                
            self.prev_buffer = slice_data   
    
            if cosine > 4.0e-07 : 
                return True
        return False

    def start (self, on_received):        
        self.s_in.bind((self.HOST, self.PORT))
    
        print("Streaming server started...")
        
        timstamp = 0
        while True:
            buffer, addr = self.s_in.recvfrom(60000)  
            data=pickle.loads(buffer)
                       
            if (len(data)>16000):               
                # if self.calculate_frame_distance(data):
                if True:
                    result = on_received(data, self.isDisplayEnabled)                    
                    if result >=0 and result !="3":
                        diff_time = time.time() -timstamp
                        print (result)
                        print(diff_time)
                        timstamp = time.time()
                        if(diff_time >0.5):
                            self.send_to_client_response(addr[0], addr[1], str(result))
                
                

       
                
                
                
  

