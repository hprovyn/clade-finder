# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 14:07:25 2020

@author: hunte
"""


from Common import CommonMethods
import sys

clades = None
levels = 1
if len(sys.argv) > 4:
    tbCladeSNPFile = sys.argv[1]
    tbSNPcladeFile = sys.argv[2]
    snpsAndOrClade = sys.argv[3].split("--")
    if len(snpsAndOrClade) == 3:
        clades = snpsAndOrClade[0].split(",")
        levels = int(snpsAndOrClade[1])
        snps = snpsAndOrClade[2].split(",")
    if len(snpsAndOrClade) == 2:
        clades = snpsAndOrClade[0].split(",")
        snps = snpsAndOrClade[1].split(",")
    if len(snpsAndOrClade) == 1:
        snps = snpsAndOrClade[0].split(",")
    #snpPanelConfigFile = sys.argv[4]
    params = sys.argv[4]
    snpPanelConfigFile = sys.argv[5]
    (positives, negatives) = CommonMethods.getEncodedPositivesNegatives(snps)
 
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
if clades:
    print(CommonMethods.getJSONForClade(params, clades, levels, positives, negatives, tbCladeSNPFile, tbSNPcladeFile))
else:
    print(CommonMethods.getJSON(params, positives, negatives, tbCladeSNPFile, tbSNPcladeFile, snpPanelConfigFile))
