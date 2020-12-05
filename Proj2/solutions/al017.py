# -*- coding: utf-8 -*-
"""
Grupo al017
Student id #93696
Student id #93750
"""

import numpy as np
import random
import math

def createdecisiontree(D,Y, noise = False):
    D = D.tolist()
    Y = Y.tolist()
    nAttributes = len(D[0])
    attributes = list(range(nAttributes))
    examples = []
    for e in range(len(D)):
        examples += [D[e] + [Y[e]]]

    tree = decisionTreeLearning(examples, attributes, examples)
    return tree


def plurality_value(examples):
    n0 = 0
    n1 = 0
    for example in examples:
        if example[-1] == 0:
            n0 += 1
        else:
            n1 += 1

    if n0 == n1:
        return random.choice([0,1])
    else:
        return 0 if n0 > n1 else 1


def allHaveSameY(examples):
    y = examples[0][-1]
    for example in examples:
        if example[-1] != y:
            return False
    return True

def getAValueExamples(examples, A, value):
    AValueExamples = [] 
    for example in examples:
        if example[A] == value:
            AValueExamples += [example]
    return AValueExamples


def Importance(attributes, examples):
    higherGain = (0, 0)
    for attribute in attributes:
        temp = Gain(attribute, examples)
        if temp > higherGain[1]:
            higherGain = (attribute, temp)

    return higherGain[0]


def Gain(attribute, examples):
    total = len(examples)
    positives = 0
    case0 = [0, 0]
    case1 = [0, 0]
    for example in examples:
        if example[-1] == 1:
            positives += 1
            if example[attribute] == 1:
                case1[0] += 1
            else:
                case1[1] += 1
        else:
            if example[attribute] == 1:
                case0[0] += 1
            else:
                case0[1] += 1

    return B(positives / total) + Remainder(case0, case1, total)


def B(q):
    if q in [0, 1]:
        return 0
        
    return -(q * math.log2(q) + (1 - q) * math.log2(1 - q))


def Remainder(case0, case1, total):
    return ((case0[0] + case0[1]) / total) * B(case0[0] / (case0[0] + case0[1]))
    

def decisionTreeLearning(examples, attributes, parent_examples):
    if not examples:
        return plurality_value(parent_examples)
    elif allHaveSameY(examples):
        return examples[0][-1]
    elif not attributes:
        return plurality_value(examples)
    else:
        A = Importance(attributes, examples)
        tree = [A]
        for value in [0,1]:
            AValueExamples = getAValueExamples(examples, A, value)
            attributesNonA = attributes[:A] + attributes[A+1:]
            subtree = decisionTreeLearning(AValueExamples, attributesNonA, examples)
            tree += [subtree]
    return tree

# D = np.array([
#                   [0,0],
#                   [0,1],
#                   [1,0],
#                   [1,1]])
# Y = np.array([0,0,0,1])
# T = createdecisiontree(D, Y)
# print(T)