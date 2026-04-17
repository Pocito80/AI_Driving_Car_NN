import matplotlib.pyplot as plt
import socket
import json
import neural_network as nn

def state_controller():
    global state
    if state == "init":
        nn_initialization()
    elif state == "ensuring_connection":
        ensure_connection()
    elif state == "running":
        running()
    elif state == "crossing":
        print("Crossing state - not implemented yet")
    elif state == "sraken":
        pass

def nn_initialization():
    global neural_network, state, sock, data, addr, neural_networks
    neural_networks = []
    for i in range(20):
        neural_network = nn.Neural_Network(3, 2, 5, 2)
        neural_networks.append(neural_network)
    state = "ensuring_connection"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 4242))
    sock.sendto("connecting".encode(), ("127.0.0.1", 4242))

    # data, addr = sock.recvfrom(65535)
    state = "ensuring_connection"

def ensure_connection():
    global state, data, addr, sock
    data, addr = sock.recvfrom(65535)
    message = data.decode()
    print(f"Received message from Godot: {message}")
    if message == "connect_requested":
        print("Received connection request from Godot, sending connection confirmation...")
        sock.sendto("ready".encode(), addr)
    elif message == "connected":
        print("Received connection confirmation from Godot, connection established!")
        sock.sendto("connected".encode(), addr)
        state = "running"

def running():
    global data, addr, sock
     # Random throttle and steer for testing
    take_raycasts()
    # commands = {}
    # 3. Send commands back to Godot
    # commands[car_id] = [random.uniform(-1, 1), random.uniform(-1, 1)]
    # sock.sendto(json.dumps(commands).encode(), addr)

def take_raycasts():
    global data, addr, sock, neural_networks, commands, state
    data, addr = sock.recvfrom(65535) 

    fleet_state = json.loads(data.decode())
    commands = {}

    if fleet_state["state"] == "standard":
        fleet_state = fleet_state["data"]

        for car in fleet_state:
            car_id = car['id']
            inputs = car['sensors']
            fitness = car['fitness']
            neural_networks[int(car_id)].forward(inputs)
            print(f"Output for car {car_id}: {neural_networks[int(car_id)].output_layer.output}")
            commands[car_id] = neural_networks[int(car_id)].output_layer.output.tolist() # Convert numpy array to list for JSON serialization
        sock.sendto(json.dumps(commands).encode(), addr)
    elif fleet_state["state"] == "restart":
        state = "init"


def main():
    global state
    state = "init"
    while True:
        state_controller()
    

if __name__ == "__main__":
    main()


# NN.get_biases()
# NN.get_model_paramiters()
# NN.get_model_paramiters()
# NN.forward(X)
# print(NN.output_layer.output)
# NN.mutate(0.05)
# NN.forward(X)
# print(NN.output_layer.output)


# kupa = [2, -4]

# print(Activation_Tanh().forward(np.array(kupa)))
# gauss = []
# for i in range(1000):
#     gauss.append(np.random.normal(0,0.0333,None))
# print(gauss)

# plt.hist(gauss, bins=20, edgecolor='black')
# plt.xlabel('Value')
# plt.ylabel('Frequency')
# plt.title('Gaussian Distribution')
# plt.show()

# NN.save_to_file("model_paramiters3.npy")
# NN.get_model_paramiters()
# NN.load_from_file("model_paramiters3.npy")
# # NN.get_model_paramiters()
# NN.forward(X)
# print(NN.output_layer.output)
# NN.save_to_file("model_paramiters3.pkl")
# NN.save_to_file("model_paramiters3.npz")

# print(np.random.rand(1))



# layer1 = Layer_Dense(4, 5)
# layer2 = Layer_Dense(5, 2)


# layer1.forward(X)
# layer2.forward(layer1.output)
# print(layer2.output)



#gauss

# sample = np.random.normal(0,0.5,None)
# print(sample)



#Point Crossover
#Uniform Crossover
#Arythmetic Crossover

#1 - 2 najlepszych zawsze kopiowanych w niezmienionej formie
#mutacja 
