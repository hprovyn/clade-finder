# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 13:22:52 2019

@author: hunte
"""

import sys
import json

if len(sys.argv) > 3:
    treeFile = sys.argv[1]
    cladeSNPFilePath = sys.argv[2]
    SNPcladeFilePath = sys.argv[3]
else:
    treeFile = "C:\clade-finder-files\yfull.json"
    cladeSNPFilePath = "C:\clade-finder-files\cladeSNPs"
    SNPcladeFilePath = "C:\clade-finder-files\SNPclades"
    
hierarchy = {}
childMap = {}
snps = {}

def parseTreeJSON(fil):
    thefile = open(fil)
    root = json.load(thefile)
    thefile.close()
    recurseTreeJson(root)
    return (root["id"])

#remove parens
#replace plus with PLUS
#replace minus with MINUS

def replaceAsNecessary(snp):
    return snp.replace("(","").replace(")","").replace("+","PLUS").replace("-","MINUS")

def parseSNPsString(snpsString):
    thesnps = set([])
    for snps in snpsString.split(", "):
        for snp in snps.split("/"):
            thesnps.add(replaceAsNecessary(snp))
    return thesnps
            
def recurseTreeJson(node):
    global hierarchy
    global snps
    global childMap
    if "children" in node:
        childMap[node["id"]] = []
        for child in node["children"]:
            if child["id"][-1] != "*":
                childMap[node["id"]].append(child["id"])
                hierarchy[child["id"]] = node["id"]
                snps[child["id"]] = parseSNPsString(child["snps"])
                recurseTreeJson(child)

def createTextFile(cladeSNPFilePath, SNPcladeFilePath):
    with open(cladeSNPFilePath, "w") as w:
        for clade in snps:
            for snp in snps[clade]:
                w.write("\t".join([clade, "1", "1", snp, "."]) + "\n")                
    w.close()
    with open(SNPcladeFilePath,  "w") as w:
        for clade in snps:
            for snp in snps[clade]:
                w.write("\t".join([snp.replace(".","_"), "1", "1", clade, "."]) + "\n")                
    w.close()    
            
parseTreeJSON(treeFile)
createTextFile(cladeSNPFilePath, SNPcladeFilePath)