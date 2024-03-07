import cv2
from hands_detection_model import HandsDetection
from client_socket import Client

class VideoCap:
    cap: cv2.VideoCapture
    hands_detection: HandsDetection
    
    def start_local(self):
        self.hands_detection = HandsDetection()
        self.hands_detection.load_model()
        self.cap = cv2.VideoCapture(0)
    
        while True:
            _, frame = self.cap.read()            
            frame = cv2.flip(frame,1 )
            framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands_detection.process(framergb)
            try:
                cv2.imshow("Ouput", result)
            except:
                cv2.imshow("Ouput", frame)
            
            if cv2.waitKey(1) == ord('q'):
                break
            
    def finish_local(self):
        self.cap.release()
        cv2.destroyAllWindows()
        
    def start_stream(self):
        self.cap = cv2.VideoCapture(0)
        client = Client()
        client.start()
        while True:
            _, frame = self.cap.read()            
            frame = cv2.flip(frame,1 )
            framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imshow("Ouput", frame)
            client.send(framergb)
            
            if cv2.waitKey(1) == ord('q'):
                break
        
    

# VideoCap().start_local()
VideoCap().start_stream()