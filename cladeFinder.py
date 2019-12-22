# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 13:19:15 2019

@author: hunte
"""

import tabix
import sys

if len(sys.argv) > 1:
    tabixFilePath = sys.argv[1]

 
#TODO get unique column values tabix query?

tb = tabix.open(tabixFilePath)

def getCladeSNPs(clade):
    
    claderesults = tb.querys(clade + ":1-1")
    snps = []
    for snp in claderesults:
        snps.append(snp[3])
    return snps

print(", ".join(getCladeSNPs("J-Z1043")))