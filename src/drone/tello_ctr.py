from djitellopy import tello
import cv2, pickle
import time
import threading
import keyboard
from client.client_socket import Client
import socket
import time


class HCTrelloController:
    isFying = False    
    prev_command = ""
    

    def init(self, isForWeb):
        print("Init")
        self.drone = tello.Tello()
        self.drone.connect()
        self.drone.streamoff()
        self.drone.streamon()
        
        if isForWeb == False:
            threadManage = threading.Thread(target=self.manage)
            threadManage.start()
        

    def fly_test(self):
        print("Ready to fly")
        battery = self.drone.get_battery()
        print ("Battery level: "+str(battery))
        try:        
            time.sleep(5)
            print ("taking off")
            self.drone.takeoff()    
            time.sleep(2)
            self.drone.go_xyz_speed(0,0,0,10)
            print("landing")
            self.drone.land()
            time.sleep(4)
        finally:
            print("emergency")
            self.drone.emergency()

    def print_state(self):
        state = self.drone.get_current_state()
        print(state)

    def manage(self):
        while True:
            try:
                key = keyboard.read_key()
                print("key: "+key)
                
                if key=="t":
                    self.drone.takeoff()
                    self.isFying = True
                elif key=="l":
                    self.drone.land()
                    self.isFying = False
                elif key=="e":
                    self.drone.emergency()
                    self.isFying = False
                elif key=="d":
                    self.drone.move_down(x=20)    
                elif key=="u":
                    self.drone.move_up(x=20)
                elif key=="up":
                    self.drone.move_forward(x=20)
                elif key=="down":
                    self.drone.move_back(x=20)
                elif key=="left":
                    self.drone.move_left(x=20)    
                elif key=="right":    
                    self.drone.move_right(x=20)    
                elif key == "a":
                    self.drone.set_speed(20)
                elif key == "b":
                    battery = self.drone.get_battery()
                    print ("Battery level: "+str(battery))
                
            except Exception as error:
                print(error)
                continue

    def manage_with_web_command(self, key):
        print(f"manage_with_web_command: {key}")
        try:
             
            if key=="t":
                self.drone.takeoff()
                self.isFying = True
            elif key=="l":
                self.drone.land()
                self.isFying = False
            elif key=="e":
                self.drone.emergency()
                self.isFying = False
            elif key=="d":
                self.drone.move_down(x=20)    
            elif key=="u":
                self.drone.move_up(x=20)
            elif key=="up":
                self.drone.move_forward(x=20)
            elif key=="down":
                self.drone.move_back(x=20)
            elif key=="left":
                self.drone.move_left(x=20)    
            elif key=="right":    
                self.drone.move_right(x=20)    
            elif key == "a":
                self.drone.set_speed(20)
            elif key == "b":
                battery = self.drone.get_battery()
                print ("Battery level: "+str(battery))
        
        except Exception as error:
            print(error)
                
         
    def drone_listener(self,command):
        try:
            print("command received: "+command)
                        
            # if (self.prev_command != command):
            if True:
                if (command =="2"):
                    if (self.isFying == False):
                        self.drone.takeoff()
                        self.isFying = True
                elif (command == "8"):
                    if (self.isFying == True):
                        self.drone.land()
                        self.isFying = False
                elif (command == "4"):
                    if (self.isFying):
                        self.drone.move_back(20)            
                elif (command == "5" or command =="7"):
                    if (self.isFying):
                        self.drone.move_forward(20) 
                elif (command == "12"):
                    if (self.isFying):
                        self.drone.rotate_clockwise(45)
                                    
        except Exception as error:
            print(error)
            return
   
    def get_frame(self):
       frame = self.drone.get_frame_read().frame
       return frame
       
    def start_stream(self):
        
        client = Client()
        client.start_listening()
        while True:
            try:
                frame = self.drone.get_frame_read().frame
                frame = cv2.flip(frame,1 )
                framergb = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
                # framergb = cv2.cvtColor(frame)
                framergb = frame
                cv2.imshow("Drone video", framergb)
                _,encoded_frame = cv2.imencode(".jpg",framergb,[int(cv2.IMWRITE_JPEG_QUALITY),30])
                buffer = pickle.dumps(encoded_frame)            
                client.send_with_listener(buffer,self.drone_listener)
                if cv2.waitKey(1) == ord('q'):
                    break 
            except:
                continue


    

    def connect_ap(self):
        # TELLO_IP = '192.168.10.1'
        # TELLO_PORT = 8889

        WIFI_SSID = 'TelloAp24'
        WIFI_PASS = 'Aa123456'
        

        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.bind(('', 9000))  # optional
               
        
        # sock.sendto("command".encode(), (TELLO_IP, TELLO_PORT))
        # time.sleep(2)        
        # sock.sendto(f'setap {WIFI_SSID} {WIFI_PASS}'.encode(), (TELLO_IP, TELLO_PORT))
        # time.sleep(2)
        state = self.drone.get_current_state()
        print(state)
        res = self.drone.send_control_command("command", 2)
        print(res)
        self.drone.connect_to_wifi(WIFI_SSID, WIFI_PASS)
       

        
        
        

# controller = HCTrelloController()
# controller.init()
# controller.start_stream()