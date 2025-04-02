from drone.sockets.web_socket_server import WebSocketServer
from drone.sockets.web_socket_client import WebSocketClient
import cv2
import threading
import time


class DroneBridge:
    port_video = 3000
    port_commands = 3500
    video_on = False

    def start_server(self):
        self.socket_server = WebSocketServer()
        self.socket_server.init("127.0.0.1", self.port_commands)
        self.socket_server.start(self.onReceiveCommand)



    def init(self):
        self.socket_client = WebSocketClient()         
        self.start_server()
       
        

    # def generate_frames_drone_camera():    
    #     drone_controller.init(True)
    #     while True:
    #         frame = drone_controller.get_frame()
    #         ret, buffer = cv2.imencode('.jpg', frame)
    #         frame = buffer.tobytes()        
    #         yield (b'--frame\r\n'
    #                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
    def start_video_streaming(self):
        print("start local camera")
        camera = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)  # Fix for macOS
        
        self.video_on = True
        while True:
            success, frame = camera.read()  # Read a frame from the camera
            if not success:
                break
            else:
                # Convert frame to JPEG format
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                self.socket_client.send_bytes(buffer.tobytes())                
             
            

    def onReceiveCommand(self, value):
        print (f"onReceiveCommand:{value}, {self.video_on}")
        
        if self.video_on == False:                                    
            self.video_on = True  
            time.sleep(2)                      
            self.socket_client.connect("00001", "127.0.0.1", self.port_video)    
            thread_stream = threading.Thread(target=self.start_video_streaming)
            thread_stream.start()


        
            
        
        
    

        
bridge = DroneBridge()
bridge.init() 
        
        




        