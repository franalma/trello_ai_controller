from ultralytics import YOLO
import pandas as pd
import cv2, pickle, struct
import cvzone
from ultralytics.solutions import distance_calculation

class TrackingModel:
    model:any
    dist_obj = distance_calculation.DistanceCalculation()
    
    def load(self):
        self.model = YOLO('yolov8n.pt')
        cap = cv2.VideoCapture(0)
    
    def track(self,frame):
        results = self.model.track(frame,persist = True)
        output = results[0].plot()                
        return output; 
    
    
    def predict(self, frame):
        results = self.model.predict(frame)
        boxes_data = results[0].boxes.data; 
        px = pd.DataFrame(boxes_data).astype("float")
        area = 0
        for index, row in px.iterrows():
            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            element_type = int(row[5])
            if (element_type == 0):
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255),2)    
                cvzone.putTextRect(frame,"person", (x1,y1),1,1)
                area = (x2-x1)*(y2-y1)                
                return [frame, area]
        return [frame,0]
            
            
       