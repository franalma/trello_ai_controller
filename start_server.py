from server_socket import Server
from hands_detection_model import HandsDetection
import cv2
import time

hands_detection = HandsDetection()
hands_detection.load_model()
prev_buffer =[]

def on_data_received(data, display):       
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
    processed_frame, class_id = hands_detection.process(frame)
    processed_frame = frame
    if display:
        try:
            cv2.imshow("Ouput", processed_frame)
        except:
            cv2.imshow("Ouput", frame) 
        
        cv2.waitKey(10) == 13   
    return class_id  

def on_data_received_fake():
    time.sleep(1)    
    return 1
                                    
server = Server()
server.start(on_received=on_data_received)