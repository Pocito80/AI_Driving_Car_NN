import numpy as np
 

np.random.seed(0)

X = [1, 2, 3, 2.5]

class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

class Activation_ReLU:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)
        return self.output

class Activation_Softmax:
    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        self.output = probabilities
        # return self.output


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
        return self.output_layer.output
    
    def get_weights(self):
        self.weights = []
        self.weights.append(self.input_layer.weights)
        for i in range(len(self.hidden_layers)):
            self.weights.append(self.hidden_layers[i].weights)
        self.weights.append(self.output_layer.weights)

    def set_weights(self, weights):
        self.input_layer.weights = weights[0]
        for i in range(len(self.hidden_layers)):
            self.hidden_layers[i].weights = weights[i+1]
        self.output_layer.weights = weights[len(weights)-1]
    
    def mutate(self, mutation_rate):
        self.get_weights()
        def mutation_process(x):
            if np.random.rand(1) <= mutation_rate:
                return x + np.random.normal(0,0.5,None)
            return x
        vectorized_mutation_process = np.vectorize(mutation_process)
        self.weights = [vectorized_mutation_process(arr) for arr in self.weights]
        self.set_weights(self.weights)



NN = Neural_Network(4, 2, 5, 2)
# NN.get_weights()
NN.mutate(0.05)
# NN.get_weights()
NN.forward(X)
print(NN.output_layer.output)

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