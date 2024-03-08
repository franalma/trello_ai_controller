from server_socket import Server
from hands_detection_model import HandsDetection
import pickle,struct
import cv2

hands_detection = HandsDetection()
hands_detection.load_model()

def on_data_received(buffer):         
    data=pickle.loads(buffer[0])
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
    processed_frame = hands_detection.process(frame)
    processed_frame = frame
    try:
        cv2.imshow("Ouput", processed_frame)
    except:
        cv2.imshow("Ouput", frame) 
    
    cv2.waitKey(10) == 13        
    
                                    
server = Server()
server.start(on_received=on_data_received)