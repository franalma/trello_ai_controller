import socket
import threading

class WebSocketClient:
    # Create a socket object
    def connect(self, droneId, address, port):
        print(f" connect WebsocketClient: {address}, {port}")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        self.client_socket.connect((address, port))

        # Send data        
        self.client_socket.sendall(droneId.encode())
        self.thread_recv = threading.Thread(target=self.start_receive)
        self.thread_recv.daemon = True
        self.thread_recv.start()
        
    
    def send(self, command):    
        self.client_socket.sendall(command.encode())

    def send_bytes(self, buffer):    
        self.client_socket.sendall(buffer)

    def start_receive(self):
        # Receive response
        while True:
            data = self.client_socket.recv(1024)
            # print("Received from server:", data.decode())



