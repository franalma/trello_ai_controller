from djitellopy import tello
import cv2
import time
import threading
import keyboard
import numpy as np
from pynput.keyboard import Key, Listener
import mediapipe as mp
from keras.models import load_model

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode = False, max_num_hands =1, min_detection_confidence = 0.7)
mp_draw = mp.solutions.drawing_utils
model = load_model("mp_hand_gesture")


# import libh264decoder

drone = tello.Tello()
startCounter = 1
drone.connect()
drone.streamoff()
drone.streamon()


def fly():
    print("Ready to fly")
    battery = drone.get_battery()
    print ("Battery level: "+str(battery))
    try:        
        time.sleep(5)
        print ("taking off")
        drone.takeoff()    
        time.sleep(2)
        drone.go_xyz_speed(0,0,0,10)
        print("landing")
        drone.land()
        time.sleep(4)
    finally:
        print("emergency")
        drone.emergency()

def print_state():
    state = drone.get_current_state()
    print(state)

def manage():
    while True:
        try:
            key = keyboard.read_key()
            print("key: "+key)
            
            if key=="t":
                drone.takeoff()
            elif key=="l":
                drone.land()
            elif key=="e":
                drone.emergency()
            elif key=="-":
                drone.move_down(x=20)    
            elif key=="+":
                drone.move_up(x=20)
            elif key=="up":
                drone.move_forward(x=20)
            elif key=="down":
                drone.move_back(x=20)
            elif key=="left":
                drone.move_left(x=20)    
            elif key=="right":    
                drone.move_right(x=20)    
            elif key == "a":
                drone.set_speed(20)
            elif key == "b":
                battery = drone.get_battery()
                print ("Battery level: "+str(battery))
                
            
            
        except Exception as error:
            print(error)
            continue
        
        
        

threadManage = threading.Thread(target=manage)
# threadManage.start()
        


while True:     
    try:
        frame = drone.get_frame_read().frame
        frame = cv2.flip(frame,1 )
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        
        # result = hands.process(framergb)
    
        # if result.multi_hand_landmarks: 
        #     x,y,c = framergb.shape
        #     landmarks = []
        #     for handslms in result.multi_hand_landmarks:
        #         for lm in handslms.landmark:
        #             lmx = int (lm.x * x)
        #             lmy = int (lm.y * y)
        #             landmarks.append([lmx, lmy])
        #         result.multi_hand_landmarks
        #         mp_draw.draw_landmarks(framergb, handslms, mp_hands.HAND_CONNECTIONS)
        #         # class_Name = labels[classID].capitalize()
        
        #     prediction = model.predict([landmarks])
        #     classID = np.argmax (prediction)        
        #     print (classID)
        #     if classID == 2: 
        #         drone.move_back(40)
        #     elif classID == 3:
        #         print("THUMB DOWN")
    
    
        print(frame)
        cv2.imshow('Video from Tellol',framergb)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            drone.streamoff()
            break
    except Exception as error:
        print (error)
        continue
