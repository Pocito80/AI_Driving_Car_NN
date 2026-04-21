import socket
import json

class Message:
    def __init__(self, type, content):
        self.data = {"type": type, 
                     "data": content}

class UDP_Server:
    def __init__(self, host="127.0.0.1", listen_port=4242, send_port=4243):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, listen_port))
        self.listen_addr = (host, listen_port)
        self.send_addr = (host, send_port)
        print(f"UDP server started on {host}:{listen_port}")

    def send_message(self, message):
        self.sock.sendto(message.encode(), self.send_addr)

    def receive_message(self):
        data, addr = self.sock.recvfrom(65535)
        return data.decode()

    def send_json(self, data):
        self.sock.sendto(json.dumps(data).encode(), self.send_addr)

    def receive_json(self):
        data, addr = self.sock.recvfrom(65535)
        return json.loads(data.decode())


