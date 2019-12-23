# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 13:19:15 2019

@author: hunte
"""

import tabix
import sys

if len(sys.argv) > 2:
    cladeSNPFilePath = sys.argv[1]
    SNPcladeFilePath = sys.argv[2]
 
#TODO get unique column values tabix query?

tbcladeSNP = tabix.open(cladeSNPFilePath)


def getCladeSNPs(clade):
    
    claderesults = tbcladeSNP.querys(clade + ":1-1")
    snps = []
    for snp in claderesults:
        snps.append(snp[3])
    return snps

print("J-Z1043", cladeSNPFilePath, SNPcladeFilePath)
print(", ".join(getCladeSNPs("J-Z1043")))

tbSNPclade = tabix.open(SNPcladeFilePath)
print(SNPcladeFilePath)
def getSNPClades(snp):
    
    SNPresults = tbSNPclade.querys(snp + ":1-1")
    clades = []
    for clade in SNPresults:
        clades.append(clade[3])
    return clades

print(", ".join(getSNPClades("M12")))
print(", ".join(getSNPClades("USP9YPLUS3636")))

def getParent(clade):
    try:
        parentResults = tbcladeSNP.querys(clade + ":2-2")
        parent = None
        for parentResult in parentResults:
            parent = parentResult[3]
        return parent
    except:
        return None

def recurseToRootAddParents(clade, hier):
    parent = getParent(clade)
    if parent != None:
        hier[clade] = parent
        if parent not in hier:
            recurseToRootAddParents(parent, hier)

def createMinimalTree(positives):
    clades = set([])
    for snp in positives:
        for clade in getSNPClades(snp):
            clades.add(clade)
    hier = {}
    for clade in clades:
        recurseToRootAddParents(clade, hier)
    return hier

hier = createMinimalTree(["PH1080","USP9YPLUS3636","Z1043"])
print(", ".join(list(hier.keys())))