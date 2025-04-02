import socket

class WebSocketServer:

    def init(self, address, port):
        # Create a TCP/IP socket
        print(f"Websocker server: {address}, {port}")
        self.port = port
        self.address = address
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the host and port
        self.server_socket.bind((address, port))


    def start(self, onReceiveCallback):
        self.server_socket.listen(1)
        print(f"Socket server listening {self.address}, {self.port}")

        # Wait for a connection
        self.conn, addr = self.server_socket.accept()
        print(f"Connected by {addr}")

        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            # print("Received:", data.decode())
            onReceiveCallback(data)
            # self.conn.sendall(data)  # Echo back the received data

        
    def finish(self):
        self.conn.close()



