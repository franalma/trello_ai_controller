import cv2
from tracking_model import TrackingModel
from tello_ctr import HCTrelloController
import time

class DroneAutoPilot:
    prev_area = 0
    drone: any
    tracking: any
    timestamp = 0
    def init(self):
        self.drone = HCTrelloController()
        self.drone.init()
        self.tracking = TrackingModel() 
        self.tracking.load()
     
        
    def start (self):                    
        while True:
            frame = self.drone.get_frame()        
            frame = cv2.flip(frame,1 )            
            display_frame, area = self.tracking.predict(frame )
            cv2.imshow("Ouput", display_frame)
            diff = time.time() - self.timestamp
            print (diff)
            print (area)
            if (diff > 2):
                if (area > 0):
                    if (area <20000 ):
                        self.drone.drone_listener("5")
                    else:
                        self.drone.drone_listener("4")
                    self.prev_area = area
                else:
                    self.drone.drone_listener("12")
                self.timestamp = time.time()              
                                
            if cv2.waitKey(1) == ord('q'):
                break    
            

autopilot = DroneAutoPilot()
autopilot.init()
autopilot.start()

           

       
                
                
                
  

