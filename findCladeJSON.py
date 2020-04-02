# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 14:07:25 2020

@author: hunte
"""


from Common import CommonMethods
import sys

if len(sys.argv) > 4:
    tbCladeSNPFile = sys.argv[1]
    tbSNPcladeFile = sys.argv[2]
    snps = sys.argv[3].split(",")
    #snpPanelConfigFile = sys.argv[4]
    params = sys.argv[4]
    positives = set([])
    negatives = set([])
    for snp in snps:
        stripped = snp.strip()
        if stripped != "":
            if stripped[-1] == "+":
                positives.add(stripped[0:-1])
            else:
                if stripped[-1] == "-":
                    negatives.add(stripped[0:-1])
 
#tbcladeSNP = tabix.open(cladeSNPFilePath)
#
#print("J-Z1043", cladeSNPFilePath, SNPcladeFilePath)
#print(", ".join(getCladeSNPs("J-Z1043")))
#
#tbSNPclade = tabix.open(SNPcladeFilePath)
#print(SNPcladeFilePath)
#
#print(", ".join(getSNPClades("M12")))
#print(", ".join(getSNPClades("USP9YPLUS3636")))

CommonMethods.getJSON(params, positives, negatives, tbCladeSNPFile, tbSNPcladeFile)