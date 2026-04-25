import matplotlib.pyplot as plt
import numpy as np


class Plot:
    def __init__(self):
        self.y_data = []
        self.x_data = []

    def update_element(self, x, y):
        self.x_data.append(x)
        self.y_data.append(y)

    def update_array(self, x_array, y_array):
        self.x_data.extend(x_array)
        self.y_data.extend(y_array)

    def show(self, title, x_label, y_label):
        plt.plot(self.x_data, self.y_data)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.grid()
        plt.show()

class Plot_Data:
    def __init__(self, x_array = [], y_array = []):
        self.x_data = x_array
        self.y_data = y_array

    def update_element(self, x, y):
        self.x_data = np.append(self.x_data, x)
        self.y_data = np.append(self.y_data, y)
       
    def safe_to_file(self, file_path):
        np.save(file_path, np.array([self.x_data, self.y_data], dtype=object), allow_pickle=True)

    def load_from_file(self, file_path):
        self.x_data, self.y_data = np.load(file_path, allow_pickle=True)



# plot = Plot()

# plot_data = Plot_Data()

# plot_data.load_from_file("plik.npy")

# print(plot_data.x_data)
# print(plot_data.y_data)

# plot_data.update_element(10, 100)

# print(plot_data.x_data)
# print(plot_data.y_data)

# np.save("plik.npy", np.array([x, y], dtype=object), allow_pickle=True)

# x, y = np.load("plik.npy", allow_pickle=True)

# # for i in range(len(x)):
# plot.update_array(x, y)

# # for gen in range(1, 11):
# #     best_fitness = gen * 10  # Simulated best fitness value for demonstration
# #     plot.update(gen, best_fitness)
# plot.show("wykres czegos od costam", "cos", "costam")