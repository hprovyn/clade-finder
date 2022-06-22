# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 14:13:00 2020

@author: hunte
"""

import sys
import time
import pandas

def createBED(pos, bedFile):
    with open(bedFile, "w") as w:
        w.write("\t".join(["chrY",str(pos-1-500),str(pos + 500)]) + "\n")
    w.close()

import subprocess
   
import multiprocessing

def executeMinimap2(referenceFile, fastQFile, pafOutputFile):
    a = subprocess.check_output(['minimap2', referenceFile, fastQFile]).decode()
    with open(pafOutputFile, "w") as w:
        w.writelines(a)
    w.close()


def parsePAF(pafOutputFile):
    fails = []
    with open(pafOutputFile, "r") as r:
        lines = r.readlines()
        for line in lines:
            splitRow = line.split("\t")
            querySeqLength = int(splitRow[1])
            targSeqName = splitRow[5]
            targStart = int(splitRow[7])
            targEnd = int(splitRow[8])
            residueMatches = int(splitRow[9])
            alignmentBlockLength = int(splitRow[10])
            minDenom = querySeqLength
            percent = float(residueMatches) / float(alignmentBlockLength)
            #if alignmentBlockLength > querySeqLength *.8:
            fails.append({"id":targSeqName, "residueMatches": residueMatches, "alignmentBlockLength": alignmentBlockLength, "differences": alignmentBlockLength - residueMatches, "percent": percent, "start": targStart, "end": targEnd})
    
    return fails

outputDir = "/var/www/html/minimap2/tmp/"
mmiDir = "/genomes/0/refseq/mt/ncbi/"
def mtdna(refIndexFile, fasta):
    pafOutputFile = outputDir + "alignment.paf"
    executeMinimap2(refIndexFile, fasta, pafOutputFile)
    return parsePAF(pafOutputFile)

class Parallelmtdna():
    def mtdna(self, theid, refIndexBase, tmpDir, fasta, fileAffix, queue):
        pafOutputFile = outputDir + tmpDir + "alignment" + fileAffix + ".paf"
        executeMinimap2(mmiDir + refIndexBase + fileAffix + ".mmi", fasta, pafOutputFile)
        queue.put(parsePAF(pafOutputFile))

def mtdna2(refIndexBase, tmpDir, fasta):
    processes = []
    queue = multiprocessing.Queue()
    results = []
    for i in range(71):
        pmtdna = Parallelmtdna()
        p = multiprocessing.Process(target=pmtdna.mtdna,args=(i,refIndexBase, tmpDir, fasta,str(i),queue))
        p.start()
        processes.append(p)
    rets = []
    for p in processes:
        ret = queue.get()
        rets.append(ret)
    for p in processes:
        p.join()
    for ret in rets:
        results = results + ret

    return results
    
def testPAF(refIndexFile, position):
    pafOutputFile = "alignment.paf"
    return parsePAF(position, pafOutputFile)

def blatOneOff(referenceFile, position):
    bedFile = "bed.bed"
    
    createBED(position, bedFile)
    blatFile = str(position) + "_BLAT"
    seq = getSequenceFromFasta(bedFile, referenceFile)
    print(seq)
    getBLAT(seq, blatFile)
    fails = parseBLAT(position, blatFile)
    if len(fails) > 0:
        return fails[0]
    else:
        return "ok"
          
from time import sleep
import json

if len(sys.argv) > 3:
    mode = sys.argv[1]
    if mode == "-batch":
        vcfFile = sys.argv[2]
        outputFile = sys.argv[3]
        referenceFile = sys.argv[4]
        analyzeNovelSNPs(vcfFile, outputFile, referenceFile)        
    else:
        if mode == "-blat":
            delay = 16
            results = []
            referenceFile = sys.argv[2]
            positions = []
            oktotal = 0
            for pos in sys.argv[3].split(","):
                positions.append(int(pos))
            for pos in positions:
                result = blatOneOff(referenceFile, pos)
                if result == "ok":
                    oktotal = oktotal + 1
                results.append(str(pos) + " " + result)
                sleep(delay)  
            for result in results:
                print(result)
            print(str(oktotal) + " of " + str(len(positions)) + " pass")
        else:
            if mode == "-minimap":
                referenceFile = sys.argv[2]
                tmpDir = sys.argv[3]
                fasta = sys.argv[4]
                start = time.time()
                results = mtdna2(referenceFile, tmpDir ,fasta)
                results.sort(key=lambda x: x['differences'], reverse=False)
                import pandas as pd
                p = pd.read_csv(mmiDir + "ncbiMap.csv")
                jerson = []
                for i in range(5):
                    theid = results[i]["id"]
                    residueMatches = results[i]['residueMatches']
                    alignmentBlockLength = results[i]['alignmentBlockLength']
                    differences = results[i]['differences']
                    percent = results[i]['percent']
                    besthg = p.loc[p['id'] == theid]['haplogroup'].values[0]
                    jerson.append({"id": theid, "hg": besthg, "differences": differences, "block": alignmentBlockLength, "percent": round(percent * 100,3)})
                end = time.time()
                response = {"matches":jerson, "seconds": end-start}
                print(json.dumps(response))
