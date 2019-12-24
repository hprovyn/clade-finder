# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 13:51:27 2019

@author: hunte
"""

from Common import CommonMethods
import sys

if len(sys.argv) > 4:
    tbCladeSNPFile = sys.argv[1]
    tbSNPcladeFile = sys.argv[2]
    positives = set(sys.argv[3].split(","))
    negatives = set(sys.argv[4].split(","))
 
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

CommonMethods.findClade(positives, negatives, tbCladeSNPFile, tbSNPcladeFile)
        
#hier = createMinimalTree(["PH1080","USP9YPLUS3636","Z1043"])
#print(", ".join(list(hier.keys())))
#
#findClade(set(["PH1080","Z1043","Z1297","M12","M241","L283","Z1825"]),set(["CTS11760","Z8429"]))