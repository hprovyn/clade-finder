# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 13:19:15 2019

@author: hunte
"""

import tabix

def getCladeSNPs(clade, tb):
    try:
        claderesults = tb.querys(clade + ":1-1")
        snps = []
        for snp in claderesults:
            snps.append(snp[3])
        return snps
    except:
        print(clade, " has no SNPs")
        return []

def getSNPClades(snp, tb):
    
    SNPresults = tb.querys(snp + ":1-1")
    clades = []
    for clade in SNPresults:
        clades.append(clade[3])
    return clades

def getParent(clade, tb):
    try:
        parentResults = tb.querys(clade + ":2-2")
        parent = None
        for parentResult in parentResults:
            parent = parentResult[3]
        if parent == '':
            return "Adam"
        return parent
    except:
        return None

def recurseToRootAddParents(clade, hier, tb):
    parent = getParent(clade, tb)
    if parent != None:
        hier[clade] = parent
        if parent not in hier:
            recurseToRootAddParents(parent, hier, tb)

def createChildMap(hier):
    childMap = {}
    for child in hier:
        if hier[child] not in childMap:
            childMap[hier[child]] = [child]
        else:
            childMap[hier[child]].append(child)
    return childMap
    
def createMinimalTree(positives, tbSNPclades, tbCladeSNPs):
    clades = set([])
    for snp in positives:
        for clade in getSNPClades(snp, tbSNPclades):
            clades.add(clade)
    hier = {}
    for clade in clades:
        recurseToRootAddParents(clade, hier, tbCladeSNPs)
    return hier

def createCladeSNPs(hierarchy, tb):
    cladeSNPs = {}
    for clade in hierarchy:
        if hierarchy[clade] not in hierarchy:
            cladeSNPs[hierarchy[clade]] = getCladeSNPs(hierarchy[clade], tb)
        cladeSNPs[clade] = getCladeSNPs(clade, tb)
    return cladeSNPs

def getTotalSequence(clade, hierarchy):
    sequence = [clade]
    thisClade = clade
    while thisClade in hierarchy:
        thisClade = hierarchy[thisClade]
        sequence.append(thisClade)
    return sequence[:-1]
    
def getScore(sequence, totalSequence):
    return float(len(sequence)) / len(totalSequence)

def printSolutions(solutions):
    for solution in solutions:
        print(" ".join(solution), getScore(solution))

def getConflicts(sequence, negatives, cladeSNPs):
    conflictingNegatives = []
    for hg in sequence:
        if any(snp in negatives for snp in cladeSNPs[hg]):
            conflictingNegativeSnps = ""
            for snp in cladeSNPs[hg]:
                if snp in negatives:
                    conflictingNegativeSnps += " " + snp
            conflictingNegatives.append(hg + " @" + conflictingNegativeSnps + ";")
    return conflictingNegatives

import numpy as np
def getPathScores(fullSequence, confirmed, negatives, positives, conflicts, cladeSNPs):
    scores = []
    for thing in fullSequence:
        if thing in confirmed:
            negs = len(negatives.intersection(set(cladeSNPs[thing])))
            poses = len(positives.intersection(set(cladeSNPs[thing])))
            toappend = 0
            if poses + negs > 0:
                toappend = float(poses) / (poses + negs)
            scores.append(toappend)
        else:
            if thing in conflicts:
                scores.append(0)
            else:
                scores.append(0.5)
    return scores

def isBasal(clade, negatives, positives, hierarchy, childMap, cladeSNPs):
    basal = False
    children = getChildren(clade, childMap)
    if len(children) > 0:
        basal = True
        for child in children:
            isNeg = len(negatives.intersection(set(cladeSNPs[child]))) > 0
            isPos = len(positives.intersection(set(cladeSNPs[child]))) > 0
            if isNeg and not isPos:
                basal = basal and True
    return basal        

def getWarningsConf(conflicts):
    messages =[]
    for conflict in conflicts:
        messages.append(" " + conflict)
    return messages

from operator import itemgetter

def getRankedSolutions(positives, negatives, hierarchy, childMap, cladeSNPs):
    solutions = []
    recurseDownTree(positives, hierarchy, childMap, cladeSNPs, solutions)
    scoredSolutions = []
    print(solutions)
    uniqueSolutions = removeDuplicates(solutions)
    print(uniqueSolutions)
    for solution in solutions:
        lastChainMoreNegThanPos = True
        removed = 0
        while lastChainMoreNegThanPos and removed < len(solution):
            totalSequence = getTotalSequence(solution[-1 - removed], hierarchy)
            totalSequence.reverse()
            conflicts = getConflicts(totalSequence, negatives, cladeSNPs)
            scores = getPathScores(totalSequence, solution, negatives, positives, conflicts, cladeSNPs)
            clade = solution[-1 - removed]
            if isBasal(clade, negatives, positives, hierarchy, childMap, cladeSNPs):
                clade = clade + "*"
            scoredSolutions.append([totalSequence, clade, np.average(scores), np.sum(scores), np.average(scores) * np.sum(scores), getWarningsConf(conflicts)])
            removed = removed + 1
            if scores[-1] > 0.5:
                lastChainMoreNegThanPos = False
            #else:
                #print(totalSequence, scores[-1], scores)
            
        #print(scoredSolutions[-1])
    scoredSolutions = sorted(scoredSolutions, key=itemgetter(4), reverse=True)
    
    return scoredSolutions

def removeDuplicates(arr): 

    n = len(arr)
    # Return, if array is  
    # empty or contains 
    # a single element 
    if n == 0 or n == 1: 
        return n 
  
    temp = list(range(n)) 
  
    # Start traversing elements 
    j = 0; 
    for i in range(0, n-1): 
  
        # If current element is 
        # not equal to next 
        # element then store that 
        # current element 
        if arr[i] != arr[i+1]: 
            temp[j] = arr[i] 
            j += 1
  
    # Store the last element 
    # as whether it is unique 
    # or repeated, it hasn't 
    # stored previously 
    temp[j] = arr[n-1] 
    j += 1
      
    # Modify original array 
    for i in range(0, j): 
        arr[i] = temp[i] 
  
    return arr

def getChildren(clade, childMap):
#    children = []
#    for child in childParents:
#        if childParents[child] == clade:
#            children.append(child)
#
    if clade in childMap:
        return childMap[clade]
    else:
        return []

def isInChildrenThisLevel(clade, positives, childMap, cladeSNPs):
    children = getChildren(clade, childMap)
    inChildren = []
    for child in children:
        if any(snp in positives for snp in cladeSNPs[child]):
            inChildren.append(child)
    return inChildren

def recurseDownTreeUntilFirstHits(clade, positives, childParents, childMap, cladeSNPs):
    posChildrenThisLevel = isInChildrenThisLevel(clade, positives, childMap, cladeSNPs)
    for child in getChildren(clade, childMap):
        if child not in posChildrenThisLevel:
            childResult = recurseDownTreeUntilFirstHits(child, positives, childParents, childMap, cladeSNPs)
            for cres in childResult:
                posChildrenThisLevel.append(cres)
    return posChildrenThisLevel

def refineHitsRecursively(sequences, positives, childParents, childMap, cladeSNPs, solutions):
    for sequence in sequences:
        refinedResults = recurseDownTreeUntilFirstHits(sequence[-1], positives, childParents, childMap, cladeSNPs)
        if len(refinedResults) == 0:
            solutions.append(sequence)
        else:
            print(sequence, refinedResults)
            for refRes in refinedResults:
                #print(sequence, refRes)
                seqCopy = sequence[:]
                seqCopy.append(refRes)
                refineHitsRecursively([seqCopy], positives, childParents, childMap, cladeSNPs, solutions)
                
def recurseDownTree(positives, childParents, childMap, cladeSNPs, solutions):
    sequences = recurseDownTreeUntilFirstHits("Adam", positives, childParents, childMap, cladeSNPs)
    newSequences = []
    for sequence in sequences:
        newSequences.append([sequence])
    refineHitsRecursively(newSequences, positives, childParents, childMap, cladeSNPs, solutions)
    
def findClade(positives, negatives, tbCladeSNPsFile, tbSNPcladesFile):
    tbSNPclades = tabix.open(tbSNPcladesFile)
    tbCladeSNPs = tabix.open(tbCladeSNPsFile)    
    hierarchy = createMinimalTree(positives, tbSNPclades, tbCladeSNPs)
    print(hierarchy)
    childMap = createChildMap(hierarchy)
    print(childMap)
    cladeSNPs = createCladeSNPs(hierarchy, tbCladeSNPs)
    print(cladeSNPs)
    b = getRankedSolutions(positives, negatives, hierarchy, childMap, cladeSNPs)
    if len(b) > 0:
        print(' computed as ', b[0][1])
    else:
        print(' unable to compute')
        

