import numpy as np

class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.2 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

class Activation_ReLU:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)
        return self.output

# class Activation_Softmax:
#     def forward(self, inputs):
#         exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
#         probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
#         self.output = probabilities

class Activation_Tanh:
    def forward(self, inputs):
        self.output = np.tanh(inputs)
        return self.output


class Neural_Network:
    def __init__(self, n_inputs, n_hidden_layers, n_hidden_layers_neurons, n_outputs):
        self.input_layer = Layer_Dense(n_inputs,n_hidden_layers_neurons)
        self.hidden_layers = []
        for i in range(n_hidden_layers):
            self.hidden_layers.append(Layer_Dense(n_hidden_layers_neurons, n_hidden_layers_neurons))
        self.output_layer = Layer_Dense(n_hidden_layers_neurons, n_outputs)
    
    def forward(self, inputs):
        self.input_layer.forward(inputs)
        hidden_output = Activation_ReLU().forward(self.input_layer.output)
        for hidden_layer in self.hidden_layers:
            hidden_layer.forward(hidden_output)
            hidden_output = Activation_ReLU().forward(hidden_layer.output)
        self.output_layer.forward(hidden_output)
        self.output_layer.output = Activation_Tanh().forward(self.output_layer.output)
        return self.output_layer.output
    
    def get_model_paramiters(self):
        self.model_paramiters = []
        self.model_paramiters.append(self.input_layer.weights)
        self.model_paramiters.append(self.input_layer.biases)
        for i in range(len(self.hidden_layers)):
            self.model_paramiters.append(self.hidden_layers[i].weights)
            self.model_paramiters.append(self.hidden_layers[i].biases)
        self.model_paramiters.append(self.output_layer.weights)
        self.model_paramiters.append(self.output_layer.biases)

    def set_model_paramiters(self, new_paramiters):
        self.input_layer.weights = new_paramiters[0]
        self.input_layer.biases = new_paramiters[1]
        for i in range(len(self.hidden_layers)):
            self.hidden_layers[i].weights = new_paramiters[(i+1)*2]
            self.hidden_layers[i].biases = new_paramiters[(i+1)*2+1]
        self.output_layer.weights = new_paramiters[len(new_paramiters)-2]
        self.output_layer.biases = new_paramiters[len(new_paramiters)-1]

    
    def mutate(self, mutation_rate):
        self.get_model_paramiters()
        def mutation_process(x):
            if np.random.rand(1) <= mutation_rate:
                return x + np.random.normal(0,0.0333,None)
            return x
        vectorized_mutation_process = np.vectorize(mutation_process)
        self.model_paramiters = [vectorized_mutation_process(arr) for arr in self.model_paramiters]
        self.set_model_paramiters(self.model_paramiters)
        

    def save_to_file(self, filename, folder):
        self.get_model_paramiters()
        np.save(f"{folder}/{filename}", np.array(self.model_paramiters, dtype=object), allow_pickle=True)

    def load_from_file(self, filename, folder):
        loaded_paramiters = np.load(f"{folder}/{filename}", allow_pickle=True)
        loaded_paramiters_list = loaded_paramiters.tolist()
        self.set_model_paramiters(loaded_paramiters_list)

    def aritmetic_crossover(self, parent1, parent2):
        parent1.get_model_paramiters()
        parent2.get_model_paramiters()
        child_paramiters = []
        for p1, p2 in zip(parent1.model_paramiters, parent2.model_paramiters):
            alpha = np.random.rand(1)
            child_paramiter = alpha * p1 + (1 - alpha) * p2
            child_paramiters.append(child_paramiter)
        self.set_model_paramiters(child_paramiters)
