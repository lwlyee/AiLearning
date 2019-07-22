#coding=utf-8
import numpy as np

def sigmoid(num):
    return 1/(1.0 + np.exp(-num))

def sigmoidDer(num):
    return np.multiply(sigmoid(num), (1-sigmoid(num)))

class network:
    def __init__(self, sizes):
        self.layerNum = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(i, 1) for i in sizes[1:]]
        self.weights = [np.random.randn(j, i) for i, j in zip(sizes[:-1], sizes[1:])]

    def forward(self, a):
        temp_input = []
        temp_out = []
        for w, b in zip(self.weights, self.biases):
            temp_input.append(a)
            a = sigmoid(np.dot(w, a))
            temp_out.append(a)
        return a, temp_input, temp_out

    def backward(self, outputs, targets, temp_input, temp_out, stepSize):
        temp_e = []
        print(abs(outputs - targets))
        index = 0
        for w, b, pre_a, out in zip(reversed(self.weights), reversed(self.biases), reversed(temp_input), reversed(temp_out)):
            if index == 0:
                e = (outputs - targets) * pre_a.T
                temp_e.append(e)
                index = 1
            else:
                e = temp_e[-1] * sigmoidDer(out) * pre_a.T
                temp_e.append(e)
            w -= stepSize * e

    def train(self, trainData, epochs, stepSize):
        inputs = np.mat(trainData)[:, :self.sizes[0]].T
        targets = np.mat(trainData)[:, self.sizes[0]:].T
        for i in range(epochs):
            outputs, temp_input, temp_out = self.forward(network, inputs)
            self.backward(self, outputs, targets, temp_input, temp_out, stepSize)
        finalPuts, _ , _ = network.forward(network, inputs)
        print("___")
        print(finalPuts)
        print(self.weights)


if __name__=='__main__':
    trainData = [[0.1, 0.5, 0.7, 0.18, 0.45, 0.37, 0.11, 0.05, 0.67]]
    network.__init__(network, [8, 4, 2, 1])
    network.train(network, trainData, 100, 0.5)

