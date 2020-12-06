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
    tree = prunning(tree)

    # print("#################### DONE 1: " + str(tree))
    if type(tree) == int:
        tree = [0, tree, tree]
    # elif (type(tree[1]) == list and type(tree[2]) == list and tree[1][0] == tree[2][0]):
    #     # print(tree[1][0])
    #     print(tree)
    #     newtree = redundance(tree[1][0], examples, attributes)
    #     treesize = len(str(tree))
    #     newtreesize = len(str(newtree))
    #     tree = tree if treesize < newtreesize else newtree
    #     print(tree)
    #     # print("#################### DONE 2: " + str(tree))


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
        # print(str(attribute) + ":" + str(temp))
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
        # print("------")
        A = Importance(attributes, examples)
        # print("------")
        tree = [A]
        # print("Choose " + str(A))
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
    
    elif type(tree[1]) == list and type(tree[1]) == list and tree[1] == tree[2]:
        tree[0] = tree[1][0]
        tree[2] = tree[1][2]
        tree[1] = tree[1][1]
    
    elif tree[1] == tree[2]:
        tree = tree[1]
        return tree
    
    tree[1] = redux(tree[1])
    tree[2] = redux(tree[2])

    return tree


def prunning(tree):
    if type(tree) == int:
        return tree
    
    elif type(tree[1]) == list and type(tree[2]) == list and tree[1][0] == tree[2][0]:
        newTree = copy.deepcopy(tree)
        newTree = switchFatherGrandFather(newTree)
        tree = redux(tree)
        newTree = redux(newTree)
        if len(str(newTree)) < len(str(tree)):
            tree = newTree
    
    tree[1] = prunning(tree[1])
    tree[2] = prunning(tree[2])

    return tree


def switchFatherGrandFather(tree):
    temp = tree[0]
    tree[0] = tree[1][0]
    tree[1][0] = temp
    tree[2][0] = temp
    temp = tree[2][1]
    tree[2][1] = tree[1][2]
    tree[1][2] = temp
    return tree


# def redundance(beginTree, examples, attributes):
#     attributes.remove(beginTree)
#     leftExamples = getAValueExamples(examples, beginTree, 0)
#     rightExamples = getAValueExamples(examples, beginTree, 1)
#     left = decisionTreeLearning(leftExamples, attributes, leftExamples)
#     right = decisionTreeLearning(rightExamples, attributes, rightExamples)

#     return [beginTree, left, right]

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
# np.random.seed(13102020)
# D = np.random.rand(5000,12)>0.5
# Y = ((D[:,1] == 0) & (D[:,6] == 0)) | ((D[:,3] == 1) & (D[:,4] == 1) | ((D[:,11] == 1) & (D[:,6] == 1)))
# T = createdecisiontree(D, Y)

# tree1 = [11,[6,[1,1,[3,0,[4,0,1]]],[4,0,[3,0,1]]],[6,[1,1,[3,0,[4,0,1]]],1]]
# tree2 = [6,[11,[1,1,[3,0,[4,0,1]]],[1,1,[3,0,[4,0,1]]]],[11,[4,0,[3,0,1]],1]]
# print(tree1)
# print(prunning(tree1))
# print(len(str(prunning(tree1))))
# print(prunning(tree2))

# tree3 = [0,[1,[3,0,1],[4,[6,[7,0,1],1],[6,[7,0,1],1]]],[2,[5,0,1],0]]
# print(prunning(tree3))
# tree3final = [0,[1,[3,0,1],[6,[7,0,1],1]],[2,[5,0,1],0]]