import socket
import json

class UDP_Server:
    def __init__(self, host="127.0.0.1", port=4242):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.addr = (host, port)
        print(f"UDP server started on {host}:{port}")

    def send_message(self, message, addr):
        self.sock.sendto(message.encode(), addr)
    def receive_message(self):
        data, addr = self.sock.recvfrom(65535)
        return data.decode()
    def send_json(self, data, addr):
        self.sock.sendto(json.dumps(data).encode(), addr)
    def receive_json(self):
        data, addr = self.sock.recvfrom(65535)
        return json.loads(data.decode())









# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(("127.0.0.1", 4242))

# while True:
#     # 1. Receive state from Godot
#     data, addr = sock.recvfrom(65535) # Larger buffer for multiple cars
#     fleet_state = json.loads(data.decode())

#     # print("Received fleet state:", fleet_state)
#     commands = {}

#     # 2. Process each car through the Neural Network
#     for car in fleet_state:
#         car_id = car['id']
#         inputs = car['sensors']
#         fitness = car['fitness']
#         print(f"Processing car {car_id} with inputs: {inputs} and fitness: {fitness}")
#         # prediction = model.predict(inputs)
#         # Example dummy output: [throttle, steer]
#         commands[car_id] = [random.uniform(-1, 1), random.uniform(-1, 1)] # Random throttle and steer for testing

#     # 3. Send commands back to Godot
#     sock.sendto(json.dumps(commands).encode(), addr)