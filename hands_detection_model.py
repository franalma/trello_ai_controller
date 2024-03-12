
import numpy as np
import mediapipe as mp
from keras.models import load_model
from server_socket import Server

class HandsDetection:
    mp_hands = mp.solutions.hands
    mp_draw:any
    model: any
    hands: any
    
    
    def load_model(self):    
        self.hands = self.mp_hands.Hands(static_image_mode = False, max_num_hands =1, min_detection_confidence = 0.7)
        self.mp_draw = mp.solutions.drawing_utils
        self.model = load_model("mp_hand_gesture")
    
    def process_movement(self, landmarks,class_id):
        try:
            print ("ClassID:"+str(class_id))
            print ("ClassID_t:"+str(type(class_id)))
            if  class_id == 3:                 
                print(landmarks)
                # print(landmarks[1].landmark)
                # print(landmarks[2].landmark)
                # print(landmarks[3].landmark)
                # print(landmarks[4].landmark)                                            
            elif class_id == 2: 
                print(landmarks)               
                # print(landmarks[1].landmark)
                # print(landmarks[2].landmark)
                # print(landmarks[3].landmark)
                # print(landmarks[4].landmark)                                                                        
            print("*******")
        except Exception as error:
            print(error)
            return
        
    
    def process(self, frame):        
        try:         
            result = self.hands.process(frame)
            x,y,c = frame.shape
            
            if result.multi_hand_landmarks:                 
                landmarks = []
                for handslms in result.multi_hand_landmarks:
                    for lm in handslms.landmark:
                        lmx = int (lm.x * x)
                        lmy = int (lm.y * y)
                        landmarks.append([lmx, lmy])
                    result.multi_hand_landmarks
                    self.mp_draw.draw_landmarks(frame, handslms, self.mp_hands.HAND_CONNECTIONS)
                                
                prediction = self.model.predict([landmarks])            
                classID = np.argmax (prediction)
                            
                return [frame, classID]

        except:
            print ("error processing")
        return [frame,-1]


                            