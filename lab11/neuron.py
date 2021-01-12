import random
from numpy import tanh, exp, heaviside
import csv


def read_input_data(filename):
    X = []
    Y = []

    with open(filename, 'r') as file:
        dataset = csv.reader(file, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)

        line1 = next(dataset)
        Nin = len(line1) - 1
        X.append(line1[0:Nin])
        Y.append(line1[Nin])

        for line in dataset:
            X.append(line[0:Nin])
            Y.append(line[Nin])
    return Nin, X, Y


class neuron():
    sigmoid = lambda x: 1 / (1 + exp(-x))
    sigmoid_prim = lambda x, s=sigmoid: s(x) * (1 - s(x))
    relu = lambda x: max(0, x)
    relu_prim = lambda x: heaviside(x, 1)
    tanh_prim = lambda x, a=tanh: 1 - a(x) ** 2

    activations = {"tanh": (tanh, tanh_prim), "sigm": (sigmoid, sigmoid_prim), "relu": (relu, relu_prim)}

    def __init__(self, input_number, activation="tanh", bias=0.0):
        self.input_number = input_number
        self.weights = [random.random() for i in range(input_number)]
        self.bias = bias
        try:
            self.activation = self.activations[activation][0]
            self.activation_derivative = self.activations[activation][1]
        except KeyError:
            print("Nie zaimplementowano takiej funkcji aktywacji: " + activation)
            exit(1)

    def train(self, epochs, X, Y, eta=0.1):
        for epoch in range(epochs):
            print("Epoch no. {}".format(epoch))

            weight_sum = sum(self.weights)

            for i in range(len(X)):
                y_out = tanh(weight_sum)

                for j in range(self.input_number):
                    self.weights[j] += eta * self.activation_derivative(weight_sum) * (Y[i] - y_out) * X[i][j]

    def output(self, input):
        sum = 0
        for index, value in enumerate(input):
            sum += value * self.weights[index]

        return self.activation(sum + self.bias)


if __name__ == '__main__':
    Nin, X, Y = read_input_data("train_data.csv")
    n = neuron(Nin)
    print(n.weights)
    print(n.output([0.2, 0.1]))
    n.train(1000, X, Y, eta=0.6)
    print(n.weights)
    print(n.output([0.15, 0.15]))
