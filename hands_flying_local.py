from hands_detection_model import HandsDetection
from tello_ctr import HCTrelloController
import cv2
import time

class HandsFlying:
    model:HandsDetection
    drone: HCTrelloController
    timestamp = 0
    
    
    def init(self):
        self.drone = HCTrelloController()
        self.model = HandsDetection()
        self.drone.init()
        self.model.load_model()
        
        
    def start(self):
        while True:
            frame = self.drone.get_frame()        
            frame = cv2.flip(frame,1 )            
            display_frame, class_id = self.model.process(frame)
            cv2.imshow("Ouput", display_frame)
            diff = time.time() - self.timestamp
         
            if diff >1:
                self.drone.drone_listener(str(class_id))
                self.timestamp = time.time()
                                 
            if cv2.waitKey(1) == ord('q'):
                break   
        
handsflying = HandsFlying()
handsflying.init()
handsflying.start()