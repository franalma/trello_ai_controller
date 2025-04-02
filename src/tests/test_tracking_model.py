

import cv2, pickle, struct
from src.models.tracking_model import TrackingModel


tracking = TrackingModel()
tracking.load()
cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()            
    frame = cv2.flip(frame,1 )     
    
    display_frame, area = tracking.predict(frame)
    cv2.imshow("Ouput", display_frame)
                
    if cv2.waitKey(1) == ord('q'):
        break 