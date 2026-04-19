from email.mime import message
import numpy as np
import matplotlib.pyplot as plt
import neural_network as nn
import UDP as udp
import time

NUMBER_OF_AGENTS = 50


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
    for i in range(NUMBER_OF_AGENTS):
        neural_network = nn.Neural_Network(6, 2, 32, 2)
        neural_networks.append(neural_network)
    state = "udp_init"
   
 
def udp_init():
    global sock, state 
    sock = udp.UDP_Server()
    state = "ensuring_connection"

def ensure_connection():
    global state, data, addr, sock
    sock.send_json(udp.Message("Connection", "Connecting_to_GD").data)
    message_recived = sock.receive_json()
    if message_recived["type"] == "Connection" and message_recived["data"] == "Connecting_to_PY":
        print("Handshake successful! We are synchronized.")
        state = "running"

def running():
    global state, message_recived


    message_recived = sock.receive_json()
    if message_recived["type"] == "FleetState":
        fleet_state = message_recived["data"]
        commands = {"data": {}}
        for car in fleet_state:
            car_id = car['id']
            inputs = car['sensors'] + [car['valocity']]
            fitness = car['fitness']
            neural_networks[int(car_id)].forward(inputs)
            # print(inputs)
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
    global state, message_recived, generation, neural_networks
    
    if generation % 50 == 0:
        for i in range(NUMBER_OF_AGENTS):
            neural_networks[i].save_to_file(f"model_paramiters_gen_{generation}_car_{i}.npy", "model3")


    top_5 = top_fitness_cars(message_recived["data"], 5)
    for rank, car in enumerate(top_5, start=1):
        print(f"{rank}. car_id={car['id']}, fitness={car['fitness']}")
   
    for i in range(NUMBER_OF_AGENTS):
        if i not in [int(car["id"]) for car in top_5]:
            # print(f"Creating new neural network {i}")
            parent1_id = np.random.randint(0, 5)
            parent2_id = np.random.randint(0, 5)
            # print(f"Selected parents for crossover: {parent1_id} and {parent2_id}")
            if parent1_id == parent2_id:
                parent2_id = (parent2_id + 1) % 5

            parent1 = neural_networks[int(top_5[parent1_id]["id"])]
            parent2 = neural_networks[int(top_5[parent2_id]["id"])]
            # print(int(top_5[parent1_id]["id"]), int(top_5[parent2_id]["id"]))
            # print(f"Performing crossover between parent {parent1_id} (fitness: {parent1.fitness}) and parent {parent2_id} (fitness: {parent2.fitness}) for child {i}")
            neural_networks[i].aritmetic_crossover(parent1, parent2)
            neural_networks[i].mutate(0.05)

    state = "ensuring_connection"

    generation += 1
    print("Generation:", generation)
    time.sleep(1)



def main():
    global state
    state = "menu"
    while True:
        state_controller()
    

if __name__ == "__main__":
    main()



#gauss

# sample = np.random.normal(0,0.5,None)
# print(sample)



#Point Crossover
#Uniform Crossover
#Arythmetic Crossover

#1 - 2 najlepszych zawsze kopiowanych w niezmienionej formie
#mutacja 
