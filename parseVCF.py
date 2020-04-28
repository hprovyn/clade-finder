# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:07:43 2020

@author: hunte
"""

import vcf
import sys

if len(sys.argv) > 1:
    vcfFile = sys.argv[1]
    
def isMale(vcfFile):
    return True

def parseBases(basesString):
    basesSplits = basesString.split("/")
    if len(basesSplits) == 2:
        call1 = basesSplits[0]
        call2 = basesSplits[1]
        if call1 == call2:
            return call1
        return None
    else:
        if len(basesSplits) == 1:
            return basesSplits[0]
    return None

def parseVCF(vcfFile):
    posAlleles = {}
    if isMale(vcfFile):    
        vcf_reader = vcf.Reader(filename=vcfFile)
        record = next(vcf_reader)
        
        
        while record:
            position = record.POS
            basesString = record.samples[0].gt_bases
            if basesString:
                parsed = parseBases(basesString)
                if parsed:
                    posAlleles[position] = parsed
                    print(str(position) + " " + parsed)
            record = next(vcf_reader)
            
    return posAlleles

parseVCF(vcfFile)