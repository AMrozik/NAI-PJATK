import random
from numpy import tanh, exp


class neuron():

    sigmoid = lambda x: 1/(1+exp(-x))
    relu = lambda x: max(0, x)
    activations = {"tanh": tanh, "sigm": sigmoid, "relu": relu}

    def __init__(self, input_number, activation="tanh", bias=0):
        self.input_number = input_number
        self.weights = [random.random() for i in range(input_number)]
        self.bias = bias
        try:
            self.activation = self.activations[activation]
        except KeyError:
            print("Nie zaimplementowano takiej funkcji aktywacji: " + activation)
            exit(1)

    # TODO: jakieś trenowanko czy coś

    def output(self, input):
        sum = 0
        for index, value in enumerate(input):
            sum += value * self.weights[index]

        # TODO: to na pewno było tak? ;p
        return self.activation(sum + self.bias)


if __name__ == '__main__':
    neuron = neuron(5)
    print(neuron.activation(0))
    print(neuron.weights)
