# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 13:22:52 2019

@author: hunte
"""

import sys
import json

if len(sys.argv) > 5:
    treeFile = sys.argv[1]
    positionMarkersTSV = sys.argv[2]
    cladeSNPFilePath = sys.argv[3]
    SNPcladeFilePath = sys.argv[4]
    positionMarkersFilePath = sys.argv[5]
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
    return snp.replace("(","").replace(")","").replace("+","PLUS").replace("-","MINUS").replace(" ","")

def parseSNPsString(snpsString):
    thesnps = set([])
    for snp in snpsString.split(", "):        
        replaced = replaceAsNecessary(snp)
        if replaced != "":
            thesnps.add(replaced)
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
            if clade in hierarchy:
                w.write("\t".join([clade, "2", "2", hierarchy[clade], "."]) + "\n")
            if clade in childMap:
                for child in childMap[clade]:
                    w.write("\t".join([clade, "3", "3", child, "."]) + "\n")
    w.close()
    with open(SNPcladeFilePath,  "w") as w:
        for clade in snps:
            for snp in snps[clade]:
                snp_replaced_dot = snp.replace(".","_")
                w.write("\t".join([snp_replaced_dot, "1", "1", clade, "."]) + "\n")
                if "/" in snp:
                    for same_name_snp in snp.split("/"):
                        w.write("\t".join([same_name_snp.replace(".","_"), "2", "2", snp_replaced_dot, "."]) + "\n")
    w.close()
    with open(positionMarkersTSV, "r") as r:
        with open(positionMarkersFilePath, "w") as w:
            for line in r.readlines():
                splt = line.replace("\n","").split("\t")
                if len(splt) == 3 and splt[0] != "":
                    marker_safe = replaceAsNecessary(splt[1]).replace(".","_")                
                    w.write("\t".join([splt[0], "1", "1", marker_safe, splt[2]]) + "\n")
                else:
                    print("ignored: " + ",".join(splt))
        w.close()
    r.close()
        
            
parseTreeJSON(treeFile)
createTextFile(cladeSNPFilePath, SNPcladeFilePath)