# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:07:43 2020

@author: hunte
"""

import vcf
import sys
import tabix
from Common import CommonMethods

def getPositionSNP(position, allele, tb):
    try:
        positionResults = tb.querys(position + ":1-1")
        for snp in positionResults:
            if snp[4] == allele:
                return snp[3], "+"
            else:
                return snp[3], "-"
        return None, None
    except:
        return None, None
        
if len(sys.argv) > 2:
    vcfFile = sys.argv[1]
    tbPositionSNPsFile = sys.argv[2]
    tbCladeSNPFile = sys.argv[3]
    tbSNPcladeFile = sys.argv[4]
    
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

def parseVCF(vcfFile, tbPositionSNPsFile):
    tbPositionSNPs = tabix.open(tbPositionSNPsFile)
    positives = []
    negatives = []
    if isMale(vcfFile):    
        vcf_reader = vcf.Reader(filename=vcfFile)
        record = next(vcf_reader)
        
        
        while record:
            if record.CHROM == "chrY":
                position = str(record.POS)
                basesString = record.samples[0].gt_bases
                if basesString:
                    allele = parseBases(basesString)
                    if allele:
                        (snp, call) = getPositionSNP(position, allele, tbPositionSNPs)
                        if snp:
                            if call == "+":
                                positives.append(snp)
                            else:
                                negatives.append(snp)
                            
            try: 
                record = next(vcf_reader)
            except:
                record = None             
    
    return positives, negatives
def getSNPsBelowClade(clade, tb):
    children = CommonMethods.getChildrenTabix(clade, tb)
    thesesnps = CommonMethods.getCladeSNPs(clade, tb)
    snps = []
    for snp in thesesnps:
        snps.append(snp)
    for child in children:
        childSNPs = getSNPsBelowClade(child, tb)
        for childSNP in childSNPs:
            snps.append(childSNP)
    return snps

def getUpstream(clade1, clade2, tbCladeSNPs):
    hier = {}
    for clade in [clade1, clade2]:
        CommonMethods.recurseToRootAddParents(clade, hier, tbCladeSNPs)
    c = clade1
    while c in hier:
        c = hier[c]
        if c == clade2:
            return clade2
    c = clade2
    while c in hier:
        c = hier[c]
        if c == clade1:
            return clade1
    return None

def filterSNPsTopTwoPredictions(jsonObj, positives, negatives, tbCladeSNPFile, tbSNPcladeFile):
    #tbCladeSNPs = tabix.open(tbCladeSNPFile)
    tbCladeSNPs = tabix.open(tbCladeSNPFile)
    tbSNPClades = tabix.open(tbSNPcladeFile)
    uniqPositives = CommonMethods.getUniqueSNPsetTabix(positives, tbSNPClades)
    uniqNegatives = CommonMethods.getUniqueSNPsetTabix(negatives, tbSNPClades)
    if "clade" in jsonObj:
        clade1 = jsonObj["clade"]
        if "nextPrediction" in jsonObj:    
            clade2 = jsonObj["nextPrediction"]["clade"]
            upstream = getUpstream(clade1, clade2, tbCladeSNPs)
            print("upstream of " + clade1  + " and " + clade2 + " is " + str(upstream))
            if upstream:
                allowed = set(getSNPsBelowClade(upstream, tbCladeSNPs))
            else:
                allowed = set(getSNPsBelowClade(clade1, tbCladeSNPs))
                allowed = allowed.union(getSNPsBelowClade(clade2, tbCladeSNPs))
        else:
            allowed = set(getSNPsBelowClade(clade1, tbCladeSNPs))
            
        filteredUniqPos = list(allowed.intersection(uniqPositives))    
        filteredUniqNeg = list(allowed.intersection(uniqNegatives))
        filteredPos = []
        for snp in filteredUniqPos:
            snpsplit = snp.split("/")
            filteredPos.append(snpsplit[0])
        filteredNeg = []
        for snp in filteredUniqNeg:
            snpsplit = snp.split("/")
            filteredNeg.append(snpsplit[0])
        return filteredPos, filteredNeg
    else:
        print(jsonObj["error"])
        return None, None
    

def makeStringFromPosNeg(positives, negatives):
    output = "+, ".join(positives)
    if len(positives) > 0:
        output = output + "+"
    if len(negatives) > 0:
        if len(positives) > 0:
            output = output + ", "
        output = output + "-, ".join(negatives)
        output = output + "-"
    return output

import time
start_time = time.time()

(positives, negatives) = parseVCF(vcfFile, tbPositionSNPsFile)
parsed_time = time.time()
print ('parsing vcf ' + str(parsed_time - start_time) + ' seconds')
jsonObj = CommonMethods.getJSONObject("score", positives, negatives, tbCladeSNPFile, tbSNPcladeFile, None)
found_time = time.time()
print ('found clade in ' + str(found_time - parsed_time) + ' seconds')
(filteredPos, filteredNeg) = filterSNPsTopTwoPredictions(jsonObj, positives, negatives, tbCladeSNPFile, tbSNPcladeFile)
#print(makeStringFromPosNeg(positives, negatives))
if filteredPos:
    filtered_time = time.time()
    print ('filtered to top two predicted in ' + str(filtered_time - found_time) + ' seconds')
    jsonObj = CommonMethods.getJSONObject("score", filteredPos, filteredPos, tbCladeSNPFile, tbSNPcladeFile, None)
    found_filter_time = time.time()
    print ('found clade filtered in ' + str(found_filter_time - filtered_time) + ' seconds')
    print(makeStringFromPosNeg(filteredPos, filteredNeg))
