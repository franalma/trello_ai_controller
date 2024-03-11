from djitellopy import tello
import cv2, pickle
import time
import threading
import keyboard
import numpy as np
from client_socket import Client


class HCTrelloController:
    drone = tello.Tello()
    

    def init(self):
        self.drone.connect()
        self.drone.streamoff()
        self.drone.streamon()
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
                elif key=="l":
                    self.drone.land()
                elif key=="e":
                    self.drone.emergency()
                elif key=="-":
                    self.drone.move_down(x=20)    
                elif key=="+":
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
         
    def drone_listener(self,command):
        print("command received: "+command)
        # if (command =="2"):
        #     self.drone.takeoff()
        # elif (command == "3"  or command == "4"):
        #     self.drone.land()
        
   
              
    def start_stream(self):
        
        client = Client()
        client.start()
        while True:
            frame = self.drone.get_frame_read().frame
            frame = cv2.flip(frame,1 )
            # framergb = cv2.cvtColor(frame,cv2.IMREAD_COLOR)
            # framergb = cv2.cvtColor(frame)
            framergb = frame
            cv2.imshow("Drone video", framergb)
            _,encoded_frame = cv2.imencode(".jpg",framergb,[int(cv2.IMWRITE_JPEG_QUALITY),30])
            buffer = pickle.dumps(encoded_frame)            
            client.send_with_listener(buffer,self.drone_listener)
            
            if cv2.waitKey(1) == ord('q'):
                break 


controller = HCTrelloController()
controller.init()
controller.start_stream()