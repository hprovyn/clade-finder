# -*- coding: utf-8 -*-
"""
Created on Tue May 31 08:50:28 2022

@author: hunte
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 17:50:06 2020

@author: hunte
"""

import sys
import subprocess

def process(fasta, outputFile):
    subprocess.check_output(["java", "-jar", haplogrepJar, "--in", fasta, "--format", "fasta", "--extend-report", "--out", outputFile])
    hg = None
    snpsString = None
    with open(outputFile, "r") as r:
        headers = r.readline()
        info = r.readline().split("\t")
        if len(info) > 2:
            hg = info[2].replace("\"","")
            snpsString = info[9].replace("\n","").replace("\"","")
    r.close()
    
    toIgnore = ["3106d"]
    if hg != None and snpsString != None:
        snps = snpsString.split(" ")
        for snp in toIgnore:
            if snp in snps:
                snps.remove(snp)
    else:
        snps = []
    return snps

def getDifferences(snps1, snps2):
    differences = []
    for snp in snps1:
        if snp in snps2:
            differences.append({"sample": snp, "match": snp})
        else:
            differences.append({"sample": snp, "match": "---"})
    for snp in snps2:
        if snp not in snps1:
            differences.append({"sample": "---", "match": snp})
    return differences
    
import json
if len(sys.argv) > 4:
        haplogrepOutputFile1 = sys.argv[1]
        haplogrepOutputFile2 = sys.argv[2]
        fastaFile1 = sys.argv[3]
        fastaFile2 = sys.argv[4]
        haplogrepJar = sys.argv[5]
        snps1 = process(fastaFile1, haplogrepOutputFile1)
        snps2 = process(fastaFile2, haplogrepOutputFile2)
        differences = getDifferences(snps1, snps2)
        print(json.dumps(differences))