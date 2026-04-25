import questionary as qt
import pathlib as path
import re
import neural_network as nn

class Menu:

    def __init__(self, title, options = None):
        self.title = title
        self.options = options or {}
    
    def display(self):
        choice = qt.select(
            self.title,
            choices=list(self.options.keys())
        ).ask()
        return self.options[choice]
    
class InputMenu(Menu):
        
    def __init__(self, title, options = None):
        super().__init__(title, options)
    
    def display(self, min_value=None, max_value=None):
        user_input = qt.text(self.title).ask()
        try:
            user_input = float(user_input)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            return self.display(min_value, max_value)
        if user_input >= min_value and user_input <= max_value:
            return user_input
        else:            
            print(f"Invalid input. Please enter a value between {min_value} and {max_value}.")
            return self.display(min_value, max_value)
        

MAIN_MENU = Menu("Select an option:", {
    "TRAINING": "training",
    "LOAD WITHOUT TRAINING": "load_without_training",
    "BACK": "back_to_previous_menu",
})


TRAINING_MENU = Menu("Select a training option:", {
    "START NEW TRAINING": "start_new_training",
    "CONTINUE TRAINING": "continue_training",
    "BACK": "back_to_previous_menu"
})

MAP_MENU = Menu("Select a map:", {
    "MAP 1": "map_1",
    "MAP 2": "map_2",
    "EXIT": "exit"
})

SPEED_MENU = Menu("Select a speed:", {
    "SLOW": "slow",
    "MEDIUM": "medium",
    "FAST": "fast",
    "BACK": "back_to_previous_menu"
})

ACTIVATION_FUNCTION_MENU = Menu("Select an activation function:", {
    "RELU": "relu",
    "SIGMOID": "sigmoid",
})

MUTATION_FUNCTION_MENU = Menu("Select a mutation function:", {  
    "POINT CROSSOVER": "point_crossover",
    "UNIFORM CROSSOVER": "uniform_crossover",
    "ARITHMETIC CROSSOVER": "arithmetic_crossover",
})

directories = [f.name for f in path.Path("Pythone_NN/Saved_models").iterdir() if f.is_dir()]
FOLDER_TREE_MENU = Menu("Select a folder to load:", {
    **{directory: directory for directory in directories},
    "BACK": "back_to_previous_menu"
})

def find_highest_generation(folder_name):
    selected_folder = path.Path(f"Pythone_NN/Saved_models/{folder_name}")
    files = [f for f in selected_folder.iterdir() if f.is_file()]

    generation_numbers = []
    for file in files:
        matches = re.findall(r"_gen_(\d+)", file.stem)
        if matches:
            generation_numbers.append(int(matches[-1]))

    highest_generation = max(generation_numbers) 
    return highest_generation

def game_paramiters_menu():
    menu = MAP_MENU
    map_choice = menu.display()
    if map_choice == "exit":
        print("Exiting program...")
        exit()
    menu = SPEED_MENU
    speed_choice = menu.display()
    if speed_choice == "back_to_previous_menu":
        game_paramiters_menu()
    print(f"Selected map: {map_choice}, Selected speed: {speed_choice}")
    main_menu()
    

def main_menu():
    menu = MAIN_MENU
    menu_choice = menu.display()
    match menu_choice:
        case "training":
            training_menu()
        case "load_without_training":
            load_without_training_menu()
        case "exit":
            print("Exiting program...")
            exit()

def training_menu():
    menu = TRAINING_MENU
    menu_choice = menu.display()
    match menu_choice:
        case "start_new_training":
            set_new_model_paramiters()
        case "continue_training":
            folder_selection_menu()
        case "back_to_previous_menu":
            main_menu()

def folder_selection_menu():
    menu = FOLDER_TREE_MENU
    folder_choice = menu.display()
    if folder_choice == "back_to_previous_menu":
        training_menu()

def load_without_training_menu():
    menu = FOLDER_TREE_MENU
    folder_choice = menu.display()
    if folder_choice == "back_to_previous_menu":
        main_menu()
    load_model_from_folder(folder_choice)
    
def load_model_from_folder(folder_name):
    highest_generation = find_highest_generation(folder_name)
    menu = Menu("Select generation to load:", {
        "Best model": "best_model_paramiters.npy",
        **{f"GENERATION {i}": i for i in range(0, highest_generation + 1, 50)},
        "BACK": "back_to_previous_menu"
    })
    generation_choice = menu.display()
    if generation_choice == "back_to_previous_menu":
        load_without_training_menu()
    print(f"Selected generation: {generation_choice}")
    
def set_new_model_paramiters():
    menu = InputMenu("Number of agents:")
    number_of_agents = int(menu.display(1,50))
    menu = InputMenu("Mutation rate (0-1):")
    mutation_rate = float(menu.display(0,1))
    menu = InputMenu("Raycast Number(3-10):")
    raycast_number = int(menu.display(3,10))
    menu = InputMenu("Hidden layer width:")
    hidden_layer_width = int(menu.display(1,100))
    menu = InputMenu("Hidden layer depth:")
    hidden_layer_depth = int(menu.display(1,10))
    menu = ACTIVATION_FUNCTION_MENU
    activation_function_choice = menu.display()
    menu = MUTATION_FUNCTION_MENU
    mutation_function_choice = menu.display()

    model_paramiters = nn.Model_Paramiters(
        number_of_agents,
        mutation_rate,
        raycast_number,
        hidden_layer_width,
        hidden_layer_depth,
        activation_function_choice,
        mutation_function_choice,
    )
    