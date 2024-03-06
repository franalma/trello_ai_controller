import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode = False, max_num_hands =1, min_detection_confidence = 0.7)
mp_draw = mp.solutions.drawing_utils
model = load_model("mp_hand_gesture")

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    x,y,c = frame.shape
    frame = cv2.flip(frame,1 )
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(framergb)
    

    
    if result.multi_hand_landmarks: 
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int (lm.x * x)
                lmy = int (lm.y * y)
                landmarks.append([lmx, lmy])
            result.multi_hand_landmarks
            mp_draw.draw_landmarks(frame, handslms, mp_hands.HAND_CONNECTIONS)
            # class_Name = labels[classID].capitalize()
    
        prediction = model.predict([landmarks])
        classID = np.argmax (prediction)
        print (classID)
        if classID == 2: 
            print("THUMB UP")
        elif classID == 3:
            print("THUMB DOWN")
        
    # cv2.putText(frame, (10,50), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    cv2.imshow("Ouput", frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
            
            