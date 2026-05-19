import matplotlib.pyplot as plt
import numpy as np


class Plot:
    def __init__(self):
        self.y_data = []
        self.x_data = []
        self.x_data2 = []
        self.y_data2 = []

    def update_element(self, x, y, x2, y2):
        self.x_data.append(x)
        self.x_data2.append(x2)
        self.y_data.append(y)
        self.y_data2.append(y2)

    def update_array(self, x_array, y_array, x2_array, y2_array):
        self.x_data.extend(x_array)
        self.x_data2.extend(x2_array)
        self.y_data.extend(y_array)
        self.y_data2.extend(y2_array)

    def show(self, title, x_label, y_label):
        plt.plot(self.x_data, self.y_data, self.x_data2, self.y_data2)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(["Average", "Best"])
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

plot = Plot()
plot_data = Plot_Data()
plot_data2 = Plot_Data()


# plot_data.load_from_file("Pythone_NN/Saved_models/model_3/best_plot_data_fitness.npy")
# plot_data2.load_from_file("Pythone_NN/Saved_models/model_3/average_plot_data_fitness.npy")

plot_data2.load_from_file("Pythone_NN/Saved_models/model_12/best_plot_data_traveled.npy")
plot_data.load_from_file("Pythone_NN/Saved_models/model_12/average_plot_data_traveled.npy")

plot.update_array(plot_data.x_data, plot_data.y_data, plot_data2.x_data, plot_data2.y_data)
# plot.show("Average traveled over generations", "Generation", "Average traveled")
