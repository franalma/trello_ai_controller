import cv2, pickle, struct
from client_socket import Client

class VideoCap:
   
    
    def start_local(self):        
        from hands_detection_model import HandsDetection
        hands_detection = HandsDetection()    
        hands_detection.load_model()
        cap = cv2.VideoCapture(0)
    
        while True:
            _, frame = cap.read()            
            frame = cv2.flip(frame,1 )
            framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands_detection.process(framergb)
            try:
                cv2.imshow("Ouput", result)
            except:
                cv2.imshow("Ouput", frame)
            
            if cv2.waitKey(1) == ord('q'):
                break
            
    # def finish_local(self):
    #     self.cap.release()
    #     cv2.destroyAllWindows()
        
    def start_stream(self):
        cap = cv2.VideoCapture(0)
        client = Client()
        client.start()
        while True:
            _, frame = cap.read()            
            frame = cv2.flip(frame,1 )
            # framergb = cv2.cvtColor(frame,cv2.IMREAD_COLOR)
            # framergb = cv2.cvtColor(frame)
            framergb = frame
            cv2.imshow("Source", framergb)
            ret,encoded_frame = cv2.imencode(".jpg",framergb,[int(cv2.IMWRITE_JPEG_QUALITY),24])
            buffer = pickle.dumps(encoded_frame)            
            client.send(buffer)
            
            if cv2.waitKey(1) == ord('q'):
                break
        
    

# VideoCap().start_local()
VideoCap().start_stream()