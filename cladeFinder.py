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

#print("J-Z1043", cladeSNPFilePath, SNPcladeFilePath)
#print(", ".join(getCladeSNPs("J-Z1043")))

tbSNPclade = tabix.open(SNPcladeFilePath)

def getSNPClades(snp):
    
    SNPresults = tbSNPclade.querys(snp + ":1-1")
    clades = []
    for clade in SNPresults:
        clades.append(clade[3])
    return clades

print(", ".join(getSNPClades("Z622")))