# -*- coding: utf-8 -*-
"""
Grupo al017
Student id #93696
Student id #93750
"""

import numpy as np
import random
import math
import copy

def createdecisiontree(D,Y, noise = False):
    D = D.astype(int).tolist()
    Y = Y.astype(int).tolist()

    nAttributes = len(D[0])
    attributes = list(range(nAttributes))
    examples = []
    for e in range(len(D)):
        examples += [D[e] + [Y[e]]]

    tree = decisionTreeLearning(examples, attributes, examples)
    tree = redux(tree)
    if type(tree) == int:
        tree = [0, tree, tree]
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
    higherGain = (attributes[0], Gain(attributes[0], examples))
    for attribute in attributes[1:]:
        temp = Gain(attribute, examples)
        if temp > higherGain[1]:
            higherGain = (attribute, temp)

    return higherGain[0]


def Gain(attribute, examples):
    total = len(examples)
    positives = 0
    pk = [0, 0]
    nk = [0, 0]
    for example in examples:
        if example[-1] == 1:
            positives += 1
            if example[attribute] == 1:
                pk[1] += 1
            else:
                pk[0] += 1
        else:
            if example[attribute] == 1:
                nk[1] += 1
            else:
                nk[0] += 1

    b = B(positives / total) 
    r = Remainder(pk, nk, total)

    return b - r


def B(q):
    if q in [0, 1]:
        return 0
        
    return -(q * math.log2(q) + (1 - q) * math.log2(1 - q))


def Remainder(pk, nk, total):
    if pk[0] + nk[0] == 0:
        p0 = 0
    else:
        p0 = ((pk[0] + nk[0]) / total) * B(pk[0] / (pk[0] + nk[0]))
    
    if pk[1] + nk[1] == 0:
        p1 = 0
    else:
        p1 = ((pk[1] + nk[1]) / total) * B(pk[1] / (pk[1] + nk[1]))

    return p0 + p1
    

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
            nattributes = copy.deepcopy(attributes)
            nattributes.remove(A)
            subtree = decisionTreeLearning(AValueExamples, nattributes, examples)
            tree += [subtree]
    return tree

def redux(tree):
    if type(tree) == int:
        return tree
    elif tree[1] == tree[2]:
        tree[0] = tree[1][0]
        tree[2] = tree[1][2]
        tree[1] = tree[1][1]
        
    tree[1] = redux(tree[1])
    tree[2] = redux(tree[2])
    return tree

# D = np.array([
#                   [0,0],
#                   [0,1],
#                   [1,0],
#                   [1,1]])
# Y = np.array([1,1,0,0])
# D3 = np.array([
#               [0,0,0,1],
#               [0,0,1,1],
#               [0,1,0,1],
#               [0,1,1,1],
#               [1,0,0,0],
#               [1,0,1,0],
#               [1,1,0,0],
#               [1,1,1,0]])
# Y = np.array([1,1,1,1,1,1,1,0])
# T = createdecisiontree(D3, Y)
# print(T)

# tree = [0,[1,[2,0,1],[2,0,1]],[1,[2,0,1],[2,0,1]]]
# tree = redux(tree)
# print(tree)
