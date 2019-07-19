#coding=utf-8
import mnist_loader as mnist_lodaer
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
        # self.weights = [np.random.randn(j, i) for i, j in zip(sizes[:-1], sizes[1:])]
        self.weights = [np.array([[0.1, 0.8], [0.4, 0.6]]), np.array([[0.3, 0.9]])]
        # print(self.weights)

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
        # print(temp_e[0].shape)
        print(abs(outputs - targets))
        index = 0
        for w, b, pre_a, out in zip(reversed(self.weights), reversed(self.biases), reversed(temp_input), reversed(temp_out)):
            if index == 0:
                # print(sigmoidDer(out).shape)
                # print(pre_a.shape)
                e = (outputs - targets) * pre_a.T
                temp_e.append(e)
                index = 1
            else:
                # print(temp_e[-1].shape)
                # print(sigmoidDer(out).shape)
                # print(pre_a.shape)
                # print(np.mat(list(temp_e)[-1]))
                e = temp_e[-1] * sigmoidDer(out) * pre_a.T
                temp_e.append(e)
            w -= stepSize * e
            # print(pre_a)
            # print(out)
            # print(np.multiply(temp_e[--1
            # print(temp_e[-1])
            # print(temp_e[-1].shape)
            # print(sigmoidDer(out).shape)
            # print(pre_a.shape)
            # print("______")
            # print(np.multiply(temp_e[-1], sigmoidDer(out)).shape)
            # e = np.multiply(temp_e[-1], sigmoidDer(out)) * pre_a.T
            # print(e)
            # print(w)
            # print(e)
            # w += e
            # temp_e.append(e)

    def train(self, trainData, epochs, stepSize):
        inputs = np.mat(trainData)[:, :self.sizes[0]].T
        targets = np.mat(trainData)[:, self.sizes[0]:].T
        for i in range(epochs):
            outputs, temp_input, temp_out = self.forward(network, inputs)
            self.backward(self, outputs, targets, temp_input, temp_out, stepSize)
        finalPuts, _, _ = network.forward(network, inputs)
        print("___")
        print(finalPuts)
        # print(self.weights)


if __name__=='__main__':
    trainData = [[0.1, 0.8, 0.7], [0.7, 0.3, 0.4]]
    network.__init__(network, [2, 2, 1])
    network.train(network, trainData, 100000, 0.5)

