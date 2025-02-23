# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:13:58 2020

@author: cm
"""

import numpy as np
from hyperparameters import Hyperparamters as hp


def error_sample(y, yp):
    return y - yp


def sigmoid(x):
    """
    sigmoid function
    """
    return 1 / (1 + np.exp(-x))


def softmax(y):
    """
    softmax function
    """
    y_exp = np.exp(y - np.max(y))
    return y_exp / np.sum(y_exp)


def sparse_softmax_cross_entropy_with_logits(logits, labels):
    """
    loss
    """
    logits = softmax(np.array(logits))
    return -np.sum(np.array(labels) * np.log(logits))# , axis=1)


def full_connection_tanh(input_, weight, bias):
    """
    1. Full connection
    2. Activation function: tanh
    """
    output = np.tanh(np.dot(input_ , weight) + bias)
    return output


def full_connection_sigmoid(input_, weight, bias):
    """
    1. Full connection
    2. Activation function: sigmoid
    """
    output = sigmoid(np.dot(input_ , weight) + bias)
    return output

def full_connection(input_, weight, bias):
    """
    1. Full connection
    2. Activation function: sigmoid
    """
    output = np.dot(input_ , weight + bias)
    return output

def tanh_derivative(y):
    """
    tanh function：1-y^2
    """
    return 1 - np.tanh(y)*np.tanh(y)


def sigmoid_derivative(y):
    """
    sigmoid function：y-y^2
    """
    return sigmoid(y) - sigmoid(y)*sigmoid(y)


def back_propagation_quadratic(W1, b1, W2, b2, error, x, output2, output1, lr):
    """
    The first activation function is the sigmoid, and the second is also sigmoid.
    Objective function：Quadratic cost 
                  f(x) = 1/2*multiply(yp-y,yp-y)
    """
    # Get the gradient in different layers
    delta2 = -error * sigmoid_derivative(output2)
    delta1 = np.dot(delta2,W2.T) * sigmoid_derivative(output1)
    # Update the weight(w2) and the biais(b2):  ΔW2 = eta*delta2*output1
    W2 = W2 - hp.lr * output1.T * delta2
    b2 = b2 - hp.lr * delta2
    # Update the weight(w1) and the biais(b1):  ΔW1 = eta*delta1*x
    W1 = W1 - hp.lr * x.T * delta1
    b1 = b1 - hp.lr * delta1
    return W1, b1, W2, b2


def back_propagation_quadratic_batch(W1, b1, W2, b2, error, x, output2, output1, lr, batch_size):
    """
    Back propagation with batch samples.
    The first activation function is the sigmoid, and the second is also sigmoid. 
    Objective function：Quadratic cost 
                  f(x) = 1/2*multiply(yp-y,yp-y)
    """
    # Get the gradient in different layers
    delta2 = - error * sigmoid_derivative(output2)
    delta1 = np.dot(delta2,W2.T) * sigmoid_derivative(output1)
    # Update the weight(w2) and the biais(b2):  ΔW2 = eta*delta2*output1
    W2 = W2 - hp.lr * np.dot(output1.T , delta2) / batch_size
    b2 = b2 - hp.lr * np.average(delta2, 0)
    # Update the weight(w1) and the biais(b1):  ΔW1 = eta*delta1*x
    W1 = W1 - hp.lr * np.dot(x.T , delta1) / batch_size
    b1 = b1 - hp.lr * np.average(delta1, 0)
    return W1, b1, W2, b2


def back_propagation_quadratic_batch_2(W1, b1, W2, b2, error, x, output2, output1, lr, batch_size):
    """
    Back propagation with batch samples.
    The first activation function is the tanh, and the second is sigmoid.
    Objective function：Quadratic cost 
                  f(x) = 1/2*(yp-y)**2
    """
    # Get the gradient in different layers
    delta2 = -error * sigmoid_derivative(output2)
    delta1 = np.dot(delta2,W2.T) * tanh_derivative(output1)    
    # Update the weight(w2) and the biais(b2):  ΔW2 = eta*delta2*output1
    W2 = W2 - hp.lr * np.dot(output1.T , delta2) / batch_size
    b2 = b2 - hp.lr * np.average(delta2, 0)
    # Update the weight(w1) and the biais(b1):  ΔW1 = eta*delta1*x
    W1 = W1 - hp.lr * np.dot(x.T , delta1) / batch_size
    b1 = b1 - hp.lr * np.average(delta1, 0)
    return W1, b1, W2, b2


def back_propagation_cross_entropy(W1, b1, W2, b2, error, x, output2, output1, lr):
    """
    The first activation function is the sigmoid, and the second is also sigmoid.
    Objective function：Cross-Entropy 
                 f(x) = -[y*ln(yp)+(1−y)ln(1−yp)]
    """
    # Get the gradient in different layers
    delta2 = -error
    delta1 = np.dot(delta2,W2.T) * sigmoid_derivative(output1)
    # Update the weight(w2) and the biais(b2):  ΔW2 = eta*delta2*output1
    W2 = W2 - hp.lr * np.dot(output1.T , delta2)
    b2 = b2 - hp.lr * delta2
    # Update the weight(w1) and the biais(b1):  ΔW1 = eta*delta1*x
    W1 = W1 - hp.lr * np.dot(x.T , delta1)
    b1 = b1 - hp.lr * delta1
    return W1, b1, W2, b2


def back_propagation_cross_entropy_batch(W1, b1, W2, b2, error, x, output2, output1, lr, batch_size):
    """
    Back propagation with batch samples.
    The first activation function is the sigmoid, and the second is also sigmoid.    
    Objective function：Cross-Entropy 
                 f(x) = -[y*ln(yp)+(1−y)ln(1−yp)]
    """
    # Get the gradient in different layers
    delta2 = -error
    delta1 = np.dot(delta2,W2.T) * sigmoid_derivative(output1)
    # Update the weight(w2) and the biais(b2):  ΔW2 = eta*delta2*output1
    W2 = W2 - hp.lr * np.dot(output1.T , delta2) / batch_size
    b2 = b2 - hp.lr * np.average(delta2, 0)
    # Update the weight(w1) and the biais(b1):  ΔW1 = eta*delta1*x
    W1 = W1 - hp.lr * np.dot(x.T , delta1) / batch_size
    b1 = b1 - hp.lr * np.average(delta1, 0)      
    return W1, b1, W2, b2


def back_propagation_cross_entropy_batch_2(W1, b1, W2, b2, error, x, output2, output1, lr, batch_size):
    """
    Back propagation with batch samples.
    The first activation function is the tanh, and the second is sigmoid.
    Objective function：Cross-Entropy 
                 f(x) = -[yln(yp)+(1−y)ln(1−yp)]
    """
    # Get the gradient in different layers
    delta2 = -error * tanh_derivative(output2)/sigmoid_derivative(output2)
    delta1 = np.dot(delta2,W2.T) * tanh_derivative(output1)
    # Update the weight(w2) and the biais(b2):  ΔW2 = eta*delta2*output1
    W2 = W2 - hp.lr * np.dot(output1.T , delta2) / batch_size
    b2 = b2 - hp.lr * np.average(delta2, 0)
    # Update the weight(w1) and the biais(b1):  ΔW1 = eta*delta1*x
    W1 = W1 - hp.lr * np.dot(x.T , delta1) / batch_size
    b1 = b1 - hp.lr * np.average(delta1, 0)     
    return W1, b1, W2, b2


if __name__ == '__main__':
    ##
    print('modules')





