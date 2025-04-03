from flask import Flask, render_template, Response,jsonify,request
import cv2

from drone.tello_ctr import HCTrelloController
from drone.sockets.web_socket_client import WebSocketClient
from drone.sockets.web_socket_server import WebSocketServer
import threading
import struct
import pickle
import socket
# from drone_bridge import DroneBridge

app = Flask(__name__)
data = b""
payload_size = struct.calcsize("Q")


def video_callback(input):
    global picture
    ret, buffer = cv2.imencode('.jpg', input)
    frame = buffer.tobytes()        
    yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
     
# # Set up socket to receive frames
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 3000))  

def receive_frames():
    global data
    while True:
        # Receive length of frame
        while len(data) < payload_size:
            packet = client_socket.recv(4096)
            if not packet:
                return
            data += packet

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        # Receive frame data
        while len(data) < msg_size:
            data += client_socket.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Decode frame
        frame = pickle.loads(frame_data)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield as MJPEG stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')



socket_commands = WebSocketClient()
socket_commands.connect("00001", "127.0.0.1", 3500)

def video_server_task():
    socket_video = WebSocketServer()
    socket_video.init("127.0.0.1", 3000)
    socket_video.start(video_callback)



           
@app.route('/')
def index():
    return render_template('index.html')  # Load HTML page

@app.route('/video_feed')
def video_feed():      
    return Response(receive_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    


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
    # video_thread = threading.Thread(target=video_server_task)
    # video_thread.daemon = True
    # video_thread.start()

    
    
    app.run(host='127.0.0.1', port=4000)
    exit()


