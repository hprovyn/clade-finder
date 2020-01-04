# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 20:28:26 2020

@author: hunte
"""

import numpy as np

def getDamerauLevenshteinDistance(a,b):
    d = np.zeros((len(a)+1, len(b)+1))
    
    for i in range(len(a)+1):
        d[i, 0] = i
    for j in range(len(b)+1):
        d[0, j] = j
    
    for i in range(len(a)):
        for j in range(len(b)):
            if a[i] == b[j]:
                cost = 0
            else:
                cost = 1
            imore = i + 1
            jmore = j + 1
            d[imore, jmore] = min(d[imore-1, jmore] + 1, #deletion
                               d[imore, jmore-1] + 1,     #insertion
                               d[imore-1, jmore-1] + cost)  #substitution
            if imore > 1 and jmore > 1 and a[i] == b[j-1] and a[i-1] == b[j]:
                d[imore, jmore] = min(d[imore, jmore],
                                   d[imore-2, jmore-2] + 1)  # transposition
    return d[len(a), len(b)]