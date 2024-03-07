from server_socket import Server
from hands_detection_model import HandsDetection

hands_detection = HandsDetection()
hands_detection.load_model()

def on_data_received(data):
    print(type(data))
    # hands_detection.process()
                                    
server = Server()
server.start(on_received=on_data_received)