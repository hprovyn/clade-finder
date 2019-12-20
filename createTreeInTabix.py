# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 13:22:52 2019

@author: hunte
"""

import sys
import json

if len(sys.argv) > 1:
    treeFile = sys.argv[1]
    tabixFilePath = sys.argv[2]
    
hierarchy = {}
childMap = {}
snps = {}

def parseTreeJSON(fil):
    thefile = open(fil)
    root = json.load(thefile)
    thefile.close()
    recurseTreeJson(root)
    return (root["id"])

def parseSNPsString(snpsString):
    thesnps = set([])
    for snps in snpsString.split(", "):
        for snp in snps.split("/"):
            thesnps.add(snp)
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

def createTextFile(outputFile):
    with open(outputFile, "w") as w:
        for clade in snps:
            for snp in snps[clade]:
                w.write("\t".join(["clade", clade, clade, snp, "."]) + "\n")
                w.write("\t".join(["SNP", snp, snp, clade, "."]) + "\n")
    w.close()