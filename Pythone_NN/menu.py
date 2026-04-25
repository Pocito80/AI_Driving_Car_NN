import questionary as qt
import pathlib as path
import re

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

# PARAMETERS_MENU = Menu("Select a parameter to adjust:", {
#     "NUMBER OF AGENTS": "number_of_agents",
#     "MUTATION RATE": "mutation_rate",
#     "BACK TO TRAINING MENU": "back_to_training_menu"
# })

directories = [f.name for f in path.Path("Pythone_NN/Saved_models").iterdir() if f.is_dir()]
FOLDER_TREE_MENU = Menu("Select a folder to load:", {
    directory: directory for directory in directories
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
 



# # choice = FILE_TREE_MENU.display()

# selected_folder = path.Path(f"Pythone_NN/Saved_models/{choice}")
# files = [f for f in selected_folder.iterdir() if f.is_file()]

# generation_numbers = []
# for file in files:
#     matches = re.findall(r"_gen_(\d+)", file.stem)
#     if matches:
#         generation_numbers.append(int(matches[-1]))

# highest_generation = max(generation_numbers) if generation_numbers else None

# # if highest_generation is not None:
# #     print(f"Najwyższy numer generacji: {highest_generation}")
# # else:
# #     print("Nie znaleziono numerów generacji w wybranym folderze.")

# GEN_MENU = Menu("Select a generation to load:", {
#     f"GENERATION {i}": i for i in range(0, highest_generation + 1, 50)
# })

# generation_choice = GEN_MENU.display()

# FILE_SELECTION_MENU = Menu("Select a file to load:", {
#     file.name: file.name for file in files
# })

