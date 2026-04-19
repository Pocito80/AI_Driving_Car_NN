from email.mime import message
import numpy as np
import matplotlib.pyplot as plt
import json
import neural_network as nn
import UDP as udp
import time


def top_fitness_cars(cars_data, count=5):
    valid = [
        car for car in cars_data
        if isinstance(car, dict) and "id" in car and "fitness" in car
    ]
    ranked = sorted(valid, key=lambda car: car["fitness"], reverse=True)
    return [{"id": car["id"], "fitness": car["fitness"]} for car in ranked[:count]]

def state_controller():
    global state

    match state:
        case "menu":
            menu()
        case "nn_init":
            nn_initialization()
        case "udp_init":
            udp_init()
        case "ensuring_connection":
            ensure_connection()
        case "running":
            running()
        case "evolution":
            evolution()

def menu():
    global state
    print("Menu state - waiting for user input to start the simulation")
    # user_input = input("Select an option: \n1. Start Simulation\n2. Exit\n")
    # match user_input:
    #     case "1":
    #         print("Starting simulation...")
    #         state = "init"
    
    state = "nn_init"


def nn_initialization():
    global state, neural_networks, generation
    generation = 0
    print("Generation:", generation)
    neural_networks = []
    for i in range(50):
        neural_network = nn.Neural_Network(3, 2, 5, 2)
        neural_networks.append(neural_network)
    state = "udp_init"
   
 
def udp_init():
    global sock, state # Short delay to ensure the server is ready before sending the first message
    sock = udp.UDP_Server()
    state = "ensuring_connection"

def ensure_connection():
    global state, data, addr, sock
    # Short delay to ensure the server is ready before sending the first message
    sock.send_json(udp.Message("Connection", "Connecting_to_GD").data)
    message_recived = sock.receive_json()
    if message_recived["type"] == "Connection" and message_recived["data"] == "Connecting_to_PY":
        print("Handshake successful! We are synchronized.")
        state = "running"

   
   
    # if message_recived["type"] == "Connection":
    #     print("Received connection confirmation from Godot, connection established!")
        # state = "running"
    # message = data.decode()
    # print(f"Received message from Godot: {message}")
    # if message == "connect_requested":
    #     print("Received connection request from Godot, sending connection confirmation...")
    #     sock.sendto("ready".encode(), addr)
    # elif message == "connected":
    #     print("Received connection confirmation from Godot, connection established!")
    #     sock.sendto("connected".encode(), addr)
    #     state = "running"

def running():
    global state, message_recived


    message_recived = sock.receive_json()
    if message_recived["type"] == "FleetState":
        fleet_state = message_recived["data"]
        commands = {"data": {}}
        for car in fleet_state:
            car_id = car['id']
            inputs = car['sensors']
            fitness = car['fitness']
            neural_networks[int(car_id)].forward(inputs)
            # print(f"Output for car {car_id}: {neural_networks[int(car_id)].output_layer.output}")
            commands["data"][car_id] = neural_networks[int(car_id)].output_layer.output.tolist() # Convert numpy array to list for JSON serialization
        sock.send_json(udp.Message("Commands", commands).data)
    elif message_recived["type"] == "Generation_Ended":
        # print("Received generation end signal from Godot, starting evolution process...")
        state = "evolution"
        for car in message_recived["data"]:
            car_id = car['id']
            fitness = car['fitness']
            # print(f"Car {car_id} fitness: {fitness}")
            neural_networks[int(car_id)].fitness = fitness


def evolution():
    global state, message_recived, generation
    
    if generation % 50 == 0:
        for i in range(50):
            neural_networks[i].save_to_file(f"model_paramiters_gen_{generation}_car_{i}.npy")


    top_5 = top_fitness_cars(message_recived["data"], 5)
    # print("Top 5 cars by fitness:")
    # for rank, car in enumerate(top_5, start=1):
    #     print(f"{rank}. car_id={car['id']}, fitness={car['fitness']}")
   
    for i in range(50):
        if i not in [int(car["id"]) for car in top_5]:
            parent1_id = np.random.randint(0, 5)
            parent2_id = np.random.randint(0, 5)
            if parent1_id == parent2_id:
                parent2_id = (parent2_id + 1) % 5
            parent1 = neural_networks[parent1_id]
            parent2 = neural_networks[parent2_id]
            neural_networks[i].aritmetic_crossover(parent1, parent2)
            neural_networks[i].mutate(0.05)

    state = "ensuring_connection"

    generation += 1
    print("Generation:", generation)
    time.sleep(1)
# def take_raycasts():
#     global state
  
   
    # fleet_state = json.loads(data.decode())
    # commands = {}

    # if fleet_state["state"] == "standard":
    #     fleet_state = fleet_state["data"]

    #     for car in fleet_state:
    #         car_id = car['id']
    #         inputs = car['sensors']
    #         fitness = car['fitness']
    #         neural_networks[int(car_id)].forward(inputs)
    #         print(f"Output for car {car_id}: {neural_networks[int(car_id)].output_layer.output}")
    #         commands[car_id] = neural_networks[int(car_id)].output_layer.output.tolist() # Convert numpy array to list for JSON serialization
    #     sock.sendto(json.dumps(commands).encode(), addr)
    # elif fleet_state["state"] == "restart":
    #     state = "init"


def main():
    global state
    state = "menu"
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
