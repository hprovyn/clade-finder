# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 18:49:11 2020

@author: hunte
"""

from Common import CommonMethods

import sys

clade = None
if len(sys.argv) > 2:
    twentyThreeAndMeFile = sys.argv[1]
    tbPositionSNPsFile = sys.argv[2]
    
snps = CommonMethods.getSNPsFrom23AndMe(twentyThreeAndMeFile, tbPositionSNPsFile)
print(", ".join(snps))