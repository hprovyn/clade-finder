# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 13:22:52 2019

@author: hunte
"""

import sys
import json

if len(sys.argv) > 6:
    treeFile = sys.argv[1]
    positionMarkersTSV = sys.argv[2]
    cladeSNPFilePath = sys.argv[3]
    SNPcladeFilePath = sys.argv[4]
    positionMarkersFilePath = sys.argv[5]
    productsFilePath = sys.argv[6]
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
    return snp.replace("(","_L_PAREN_").replace(")","_R_PAREN_").replace("+","_PLUS_").replace("-","_MINUS_").replace(" ","").replace(".","_DOT_")

toIgnore = ["PF6234"]
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

def createTextFile(cladeSNPFilePath, SNPcladeFilePath, uniqSnpToProducts):
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
                w.write("\t".join([snp, "1", "1", clade, "."]) + "\n")
                if "/" in snp:
                    for same_name_snp in snp.split("/"):
                        if same_name_snp not in toIgnore:
                            w.write("\t".join([same_name_snp, "2", "2", snp, "."]) + "\n")
        for uniqSNP in uniqSnpToProducts:
            w.write("\t".join([uniqSNP, "3", "3", uniqSnpToProducts[uniqSNP], "."]) + "\n")
    w.close()
    with open(positionMarkersTSV, "r") as r:
        with open(positionMarkersFilePath, "w") as w:
            for line in r.readlines():
                splt = line.replace("\n","").split("\t")
                if len(splt) == 3 and splt[0] != "":
                    marker_safe = replaceAsNecessary(splt[1])             
                    w.write("\t".join([splt[0], "1", "1", marker_safe, splt[2]]) + "\n")
                else:
                    print("ignored: " + ",".join(splt))
        w.close()
    r.close()
        

def getMappingOfSamenameSNPtoUniq():
    
    uniqsnps = set([])
    for clade in snps:
        for snp in snps[clade]:
            uniqsnps.add(snp)
    samenameSNPToUniqSNP = {}
    for snp in uniqsnps:
        if "/" in snp:
            samenamesnps = snp.split("/")
            for samenamesnp in samenamesnps:
                samenameSNPToUniqSNP[samenamesnp] = snp
    
    return samenameSNPToUniqSNP

def getUniqSNPtoProducts(productsFilePath):
    snpToProducts = {}
    with open(productsFilePath, "r") as r:
        for line in r.readlines():
            splt = line.replace("\n","").split("\t")
            if len(splt) == 2:
                snp = replaceAsNecessary(splt[0])
                snpToProducts[snp] = splt[1]
    r.close()
    uniqSNPtoProducts = {}
    samenameSNPtoUniqSNP = getMappingOfSamenameSNPtoUniq()
    for snp in snpToProducts:
        if snp in samenameSNPtoUniqSNP:
            uniqSNPtoProducts[samenameSNPtoUniqSNP[snp]] = snpToProducts[snp]
        else:
            uniqSNPtoProducts[snp] = snpToProducts[snp]
    return uniqSNPtoProducts

           
parseTreeJSON(treeFile)
uniqSnpToProducts = getUniqSNPtoProducts(productsFilePath)
createTextFile(cladeSNPFilePath, SNPcladeFilePath, uniqSnpToProducts)