from flask import Flask, render_template, Response,jsonify,request
import cv2

from drone.tello_ctr import HCTrelloController
from drone.sockets.web_socket_client import WebSocketClient
from drone.sockets.web_socket_server import WebSocketServer
import threading
# from drone_bridge import DroneBridge

app = Flask(__name__)

# OpenCV Video Capture (0 = default camera)

picture = b""
def video_callback(buffer):
   global picture
   picture = buffer
     
    

# drone_controller = HCTrelloController()
socket_commands = WebSocketClient()
socket_commands.connect("00001", "127.0.0.1", 3500)

def video_server_task():
    socket_video = WebSocketServer()
    socket_video.init("127.0.0.1", 3000)
    socket_video.start(video_callback)



# def generate_frames_drone_camera():    
#     drone_controller.init(True)
#     while True:
#         frame = drone_controller.get_frame()
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()        
#         yield (b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        



           
@app.route('/')
def index():
    return render_template('index.html')  # Load HTML page

@app.route('/video_feed')
def video_feed():  
    yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + picture + b'\r\n')
    return Response(picture, mimetype='multipart/x-mixed-replace; boundary=frame')
    
    


@app.route('/drone-control', methods=['POST'])
def drone_control():
    data = request.json
    command = data.get("command")
    print(f"command received:{command}")
    
    socket_commands.send(command)
    return jsonify({"status": "ok"}), 200


@app.route('/drone-api', methods=['POST'])
def drone_api():
    data = request.json
    command = data.get("command")
    print(f"command received:{command}")
    if (command == "bat"):
        socket_commands.send("bat")
        return jsonify({"command": "battery"}), 200


    
    return jsonify({}), 404



if __name__ == "__main__":
    video_thread = threading.Thread(target=video_server_task)
    video_thread.daemon = True
    video_thread.start()

    
    
    app.run(host='127.0.0.1', port=4000)
    exit()


