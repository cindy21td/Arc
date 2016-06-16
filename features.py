# Name:     Marcella Cindy Prasetio
# ID  :     1335797
# mcp21@cs.washington.edu
#
# CSE 490U - Homework 5
#
# Modules for generating feature templates and
# feature-based operations

from random import gauss
import numpy as np
from scipy.sparse import csr_matrix


# HYPER PARAMETERS
# Minimum number of feature occurrence
k = 3
# Mean for W random generation
MU = 0
# Standard deviation for W random generation
STD = 1


# Returns previous, current, and next token of the given indexes
def get_triple(sen, i, j, length):
    curr = sen[i][j]
    prev = None
    if i > 0:
        prev = sen[i-1][j]
    next = None
    if i < length - 1:
        next = sen[i+1][j]

    return (prev, curr, next)


# Collects and returns the feature templates for given token at index i
def collect_feature(sen, i, tag_prev, tag_curr):
    feat = []

    # word
    word = get_triple(sen, i, 0, len(sen))
    # pos tags
    pos = get_triple(sen, i, 1, len(sen))
    # syn tags
    syn = get_triple(sen, i, 2, len(sen))

    feat.append((word[1]))
    feat.append((any(i.isdigit() for i in word[1]), tag_curr))
    feat.append((word[1][0].isupper(), pos[0]))
    feat.append((word[1], tag_prev, tag_curr))
    feat.append((pos[1], tag_prev, tag_curr))

    # WORD
    # unigram
    feat.append((word[1], tag_curr))
    # bigram before
    feat.append((word[0], word[1], tag_prev, tag_curr))
    # bigram after
    feat.append((word[1], word[2], tag_prev, tag_curr))
    

    # POS
    # unigram
    feat.append((pos[1], tag_curr))
    # bigram before
    feat.append((pos[0], pos[1], tag_prev, tag_curr))
    # bigram after
    feat.append((pos[1], pos[2], tag_prev, tag_curr))


    # SYN
    # unigram
    #feat.append((syn[1], tag_curr))
    # bigram before
    #feat.append((syn[0], syn[1], tag_prev, tag_curr))
    # bigram after
    #feat.append((syn[1], syn[2], tag_prev, tag_curr))
    
    
    # TAG
    feat.append((tag_prev, tag_curr))

    return feat


# Returns phi for given x, i, previous and current tags
def phi(x, i, tag_prev, tag_curr):
    feat = collect_feature(x, i, tag_prev, tag_curr)
    
    return feat


# Returns Phi(x, y)
def total_phi(x, y):
    Phi = {}

    tag_prev = None
    for i in range(0, len(x)):
        feat = phi(x, i, tag_prev, y[i])
        for f in feat:
            if f not in Phi:
                Phi[f] = 0
            Phi[f] += 1
        tag_prev = y[i]
    return Phi


# Cleans the given dct by removing elements that has a value less than k
def clean_dict(dct, k):
    lost = []
    for (key, v) in dct.items():
        if v < k:
            lost.append(key)
        else:
            dct[key] = gauss(MU, STD)
            #dct[key] = 0

    for l in lost:
        del dct[l]


# Builds and returns a feature vector template from the given data
def build_vector_template(data):
    temp = {}
    tags = []

    # iterate each sentence
    for d in data:
        for i in range(0, len(d)):
            tag = d[i][3]
            if tag not in tags:
                tags.append(tag)

            tag_prev = None
            if i > 0:
            	tag_prev = d[i-1][3]

            feat = collect_feature(d, i, tag_prev, tag)
            for f in feat:
                if f not in temp:
                    temp[f] = 0
                temp[f] += 1

    clean_dict(temp, k)

    return temp, sorted(tags)
