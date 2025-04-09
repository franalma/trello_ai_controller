from drone.sockets.web_socket_server import WebSocketServer
from drone.tello_ctr import HCTrelloController
import cv2
import threading
import time
import socket
import struct
import pickle
from models.hands_detection_model import HandsDetection


class DroneBridge:
    port_video = 3000
    port_commands = 3500
    video_on = False
    drone_controller = HCTrelloController()
    hands_model = HandsDetection()
    server_video = "127.0.0.1"
    server_commands = "127.0.0.1"

    def start_command_server(self):
        self.socket_server = WebSocketServer()
        self.socket_server.init(self.server_commands, self.port_commands)
        self.socket_server.start(self.onReceiveCommand)


    def start_video_server_local_camera(self):
        # Setup socket server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.server_video, self.port_video))
        server_socket.listen(1)
        print(f"Waiting for connection, port {self.port_video}")
        conn, addr = server_socket.accept()
        print("Connected to:", addr)

        # Capture from webcam (or replace with video file)
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Serialize frame
            data = pickle.dumps(frame)
            size = struct.pack("Q", len(data))  # 8-byte header
            conn.sendall(size + data)
       


    def start_video_drone(self):
        # Setup socket server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.server_video, self.port_video))
        server_socket.listen(1)
        print(f"Waiting for connection, port {self.port_video}")
        conn, addr = server_socket.accept()
        print("Connected to:", addr)
       
        while True:
            try:
                frame = self.drone_controller.get_frame()
                data = pickle.dumps(frame)
                # frame_p, class_id = self.hands_model.process(frame)
                # Serialize frame
                # data = pickle.dumps(frame_p)
                size = struct.pack("Q", len(data))  # 8-byte header
                conn.sendall(size + data)
            except Exception as e: 
                continue
                




    def init(self):
        # self.start_command_server()

        thread_commands = threading.Thread(target=self.start_command_server)        
        thread_commands.start()

        # thread_video = threading.Thread(target=self.start_video_server_local_camera)        
        # thread_video.start()

        self.hands_model.load_model()
        thread_video = threading.Thread(target=self.start_video_drone)        
        thread_video.start()

        self.drone_controller.init(True)


        
        
       
        

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
        str_value  = value.decode('utf-8')
        print (f"onReceiveCommand:{str_value}, {self.video_on}")

        self.drone_controller.manage_with_web_command(str_value)
            

        
    
bridge = DroneBridge()
bridge.init() 
        
        




        