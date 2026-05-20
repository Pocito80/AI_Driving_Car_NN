import numpy as np
import neural_network as nn
import udp
import time
import plot as pl
import menu as m
import json
import os
import re


class Symulation_Values:
    def __init__(self, state, train, path, to_load, map, game_speed, generation, model_paramiters):
        self.state = state
        self.train = train
        self.path = path
        self.to_load = to_load
        self.map = map
        self.game_speed = game_speed
        self.generation = generation
        self.model_paramiters = model_paramiters

    def to_dict(self):
        return {
            "state": self.state,
            "train": self.train,
            "path": self.path,
            "to_load": self.to_load,
            "map": self.map,
            "game_speed": self.game_speed,
            "generation": self.generation,
            "model_paramiters": self.model_paramiters.to_dict() if self.model_paramiters else None
        }


def top_fitness_cars(cars_data, count=5):
    valid = [
        car for car in cars_data
        if isinstance(car, dict) and "id" in car and "fitness" in car and "traveled" in car
    ]
    ranked = sorted(valid, key=lambda car: car["fitness"], reverse=True)
    return [{"id": car["id"], "fitness": car["fitness"], "traveled": car["traveled"]} for car in ranked[:count]]


def state_controller():
    global state, symulation_values
    if symulation_values.state == "selection_done":
        state = "file_loading"
        symulation_values.state = ""

    match state:
        case "menu":
            m.game_paramiters_menu(symulation_values)
        case "file_loading":
            load_paramiters_from_file()
        case "nn_init":
            nn_initialization()
        case "plot_init":
            plot_initialization()
        case "udp_init":
            udp_init()
        case "ensuring_connection":
            ensure_connection()
        case "sendig_paramiters":
            send_paramiters()
        case "running":
            running()
        case "saving_generation_data":
            saving_generation_data()
        case "evolution":
            evolution()

def load_paramiters_from_file():
    global state, symulation_values, save_path

    if symulation_values.to_load:
      
        folder_name = symulation_values.path.split("/")[0]
        with open(f"Python_NN/Saved_models/{folder_name}/paramiters.json", "r") as f:
            paramiters_data = json.load(f)
            model_paramiters = nn.Model_Paramiters(
                paramiters_data["number_of_agents"],
                paramiters_data["mutation_rate"],
                paramiters_data["raycast_number"],
                paramiters_data["hidden_layer_width"],
                paramiters_data["hidden_layer_depth"],
                paramiters_data["activation_function"],
                paramiters_data["mutation_function"],
                paramiters_data["best_fittness"]
            )
            symulation_values.model_paramiters = model_paramiters
            save_path = f"Python_NN/Saved_models/{folder_name}"
    else:
        max_folder_number = get_max_folder_number("Python_NN/Saved_models")
        folder_name = f"model_{max_folder_number+1}"
        folder_path = f"Python_NN/Saved_models/{folder_name}"
        os.makedirs(folder_path, exist_ok=True)
        with open(f"Python_NN/Saved_models/{folder_name}/paramiters.json", "w") as f:
            json.dump(symulation_values.model_paramiters.to_dict(), f)
        save_path = folder_path
   
    state = "nn_init"

def get_max_folder_number(directory_path):
    folders = os.listdir(directory_path)
    numbers = []
    for name in folders:
        match = re.search(r'(\d+)', name)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers) if numbers else 0


def nn_initialization():
    global state, neural_networks, generation, best_time, plot, symulation_values

    generation = symulation_values.generation
    neural_networks = []

    if symulation_values.to_load and symulation_values.path.split("/")[1] == "best_model_paramiters.npy":
        symulation_values.model_paramiters.number_of_agents = 1
        path = f"Python_NN/Saved_models/{symulation_values.path}"
    elif symulation_values.to_load:
        path = f"Python_NN/Saved_models/{symulation_values.path}_car_{{0}}.npy"
        generation = int(symulation_values.path.split("_")[4])

    for i in range(symulation_values.model_paramiters.number_of_agents):
        neural_network = nn.Neural_Network(symulation_values.model_paramiters.raycast_number+1, symulation_values.model_paramiters.hidden_layer_depth, symulation_values.model_paramiters.hidden_layer_width, 2, symulation_values.model_paramiters.activation_function)
        neural_networks.append(neural_network)
        if symulation_values.to_load:
            neural_network.load_from_file(path.replace("{0}", str(i)))
    
    state = "plot_init" if symulation_values.train else "udp_init"
 
def plot_initialization():
    global best_plot_data_fitness, average_plot_data_fitness, best_plot_data_traveled, average_plot_data_traveled,state

    best_plot_data_fitness = pl.Plot_Data()
    average_plot_data_fitness = pl.Plot_Data()
    best_plot_data_traveled = pl.Plot_Data()
    average_plot_data_traveled = pl.Plot_Data()

    if symulation_values.to_load:
        load_and_trim(best_plot_data_fitness, f"{save_path}/best_plot_data_fitness.npy")
        load_and_trim(average_plot_data_fitness, f"{save_path}/average_plot_data_fitness.npy")
        load_and_trim(best_plot_data_traveled, f"{save_path}/best_plot_data_traveled.npy")
        load_and_trim(average_plot_data_traveled, f"{save_path}/average_plot_data_traveled.npy")
    
    state = "udp_init"

def load_and_trim(plot, filename):
    plot.load_from_file(filename)
    if generation is not None:
        plot.x_data = plot.x_data[:generation]
        plot.y_data = plot.y_data[:generation]


def udp_init():
    global sock, state 
    sock = udp.UDP_Server()
    state = "ensuring_connection"

def ensure_connection():
    global state, data, addr, sock
    sock.send_json(udp.Message("Connection", "Connecting_to_GD").data)
    message_recived = sock.receive_json()
    if message_recived["type"] == "Connection" and message_recived["data"] == "Connecting_to_PY":
        state = "sendig_paramiters"

def send_paramiters():
    global state, symulation_values, sock
    sock.send_json(udp.Message("Paramiters", symulation_values.to_dict()).data)
    message_recived = sock.receive_json()
    if message_recived["type"] == "Paramiters" and message_recived["data"] == "Paramiters_received":
        state = "running"

def running():
    global state, message_recived

    message_recived = sock.receive_json()
    if message_recived["type"] == "FleetState":
        fleet_state = message_recived["data"]
        commands = {"data": {}}
        for car in fleet_state:
            car_id = car['id']
            inputs = car['sensors'] + [car['velocity']]
            fitness = car['fitness']
            neural_networks[int(car_id)].forward(inputs)
            commands["data"][car_id] = neural_networks[int(car_id)].output_layer.output.tolist()
        sock.send_json(udp.Message("Commands", commands).data)

    elif message_recived["type"] == "Generation_Ended":
        if symulation_values.train:
            state = "saving_generation_data"
            for car in message_recived["data"]:
                car_id = car['id']
                fitness = car['fitness']
                neural_networks[int(car_id)].fitness = fitness
        else:
            state = "ensuring_connection"
            time.sleep(0.5)

def saving_generation_data():
    global state, message_recived, top_5

    print("Generation:", generation)
    top_5 = top_fitness_cars(message_recived["data"], 5)
    print_top_5_cars(top_5)
    save_plot_data()
    save_best_model()
    save_model_paramiters_to_file()

    state = "evolution"

def evolution():
    global state, message_recived, generation, neural_networks, top_5
    
    for i in range(symulation_values.model_paramiters.number_of_agents):
        if i not in [int(car["id"]) for car in top_5]:
            parent1_id = np.random.randint(0, 5)
            parent2_id = np.random.randint(0, 5)
            if parent1_id == parent2_id:
                parent2_id = (parent2_id + 1) % 5

            parent1 = neural_networks[int(top_5[parent1_id]["id"])]
            parent2 = neural_networks[int(top_5[parent2_id]["id"])]
            
            if symulation_values.model_paramiters.mutation_function == "uniform_crossover":
                neural_networks[i].uniform_crossover(parent1, parent2)
            elif symulation_values.model_paramiters.mutation_function == "arithmetic_crossover":
                neural_networks[i].arithmetic_crossover(parent1, parent2)
            neural_networks[i].mutate(symulation_values.model_paramiters.mutation_rate)

    state = "ensuring_connection"

    generation += 1
    time.sleep(0.5)

def save_model_paramiters_to_file():
    global neural_networks, generation, save_path
    if generation % 50 == 0:
        for i in range(symulation_values.model_paramiters.number_of_agents):
            neural_networks[i].save_to_file(save_path + f"/model_paramiters_gen_{generation}_car_{i}.npy")

def print_top_5_cars(top_5):
    for i, car in enumerate(top_5):
        print(f"{i+1}. Car ID: {car['id']}, Fitness: {car['fitness']}, Traveled: {car['traveled']}")

def save_plot_data():
    global message_recived, generation, best_plot_data_fitness, average_plot_data_fitness, best_plot_data_traveled, average_plot_data_traveled, save_path, top_5

    best_plot_data_fitness.update_element(generation, top_5[0]["fitness"])
    average_fitness = sum(car['fitness'] for car in message_recived["data"]) / len(message_recived["data"])
    average_plot_data_fitness.update_element(generation, average_fitness)
    np.save(save_path + "/best_plot_data_fitness.npy", np.array([best_plot_data_fitness.x_data, best_plot_data_fitness.y_data], dtype=object), allow_pickle=True)
    np.save(save_path + "/average_plot_data_fitness.npy", np.array([average_plot_data_fitness.x_data, average_plot_data_fitness.y_data], dtype=object), allow_pickle=True)
    best_plot_data_traveled.update_element(generation, top_5[0]["traveled"])
    average_traveled = sum(car['traveled'] for car in message_recived["data"]) / len(message_recived["data"])
    average_plot_data_traveled.update_element(generation, average_traveled)
    np.save(save_path + "/best_plot_data_traveled.npy", np.array([best_plot_data_traveled.x_data, best_plot_data_traveled.y_data], dtype=object), allow_pickle=True)
    np.save(save_path + "/average_plot_data_traveled.npy", np.array([average_plot_data_traveled.x_data, average_plot_data_traveled.y_data], dtype=object), allow_pickle=True)

def save_best_model():
    global top_5, symulation_values, save_path

    if top_5[0]["fitness"] > symulation_values.model_paramiters.best_fittness:
        symulation_values.model_paramiters.best_fittness = top_5[0]["fitness"]
        neural_networks[int(top_5[0]["id"])].save_to_file(save_path + f"/best_model_paramiters.npy")
        with open(save_path + "/paramiters.json", "r") as f:
            paramiters_data = json.load(f)
        paramiters_data["best_fittness"] = symulation_values.model_paramiters.best_fittness
        with open(save_path + "/paramiters.json", "w") as f:
            json.dump(paramiters_data, f)
        print(f"New best fitness: {symulation_values.model_paramiters.best_fittness}")

def main():
    global state, model_paramiters, symulation_values

    state = "menu"
    model_paramiters = nn.Model_Paramiters(0,0,0,0,0,"","")
    symulation_values = Symulation_Values("menu", False, "", "", False, 0, 0, model_paramiters)
    while True:
        state_controller()

if __name__ == "__main__":
    main()

