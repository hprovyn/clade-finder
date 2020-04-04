# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 13:19:15 2019

@author: hunte
"""

import tabix

def getCladeSNPs(clade, tb):
    try:
        claderesults = tb.querys(clade + ":1-1")
        snps = []
        for snp in claderesults:
            snps.append(snp[3])
        return snps
    except:
        print(clade, " has no SNPs")
        return []

def getSNPClades(snp, tb):
    try:
        SNPresults = tb.querys(snp + ":1-1")
        clades = []
        for clade in SNPresults:
            clades.append(clade[3])
        return clades
    except:
        return []
    
def getParentTabix(clade, tb):
    try:
        parentResults = tb.querys(clade + ":2-2")
        parent = None
        for parentResult in parentResults:
            parent = parentResult[3]
        if parent == '':
            return "Adam"
        return parent
    except:
        return None

def getChildrenTabix(clade, tb):
    try:
        childResults = tb.querys(clade + ":3-3")
        children = []
        for childResult in childResults:
            child = childResult[3]
            children.append(child)
        return children
    except:
        return []
    
def getUniqueSNPTabix(snp, tb):
    returnvalue = snp
    try:
        uniqueSNPResults = tb.querys(snp + ":2-2")
        for uniqueSNPResult in uniqueSNPResults:
            if uniqueSNPResult is not None and len(uniqueSNPResult) > 3 and uniqueSNPResult[3] is not None:
                returnvalue = uniqueSNPResult[3]
    finally:
        return returnvalue
    
def getUniqueSNPsetTabix(snps, tb):
    uniqueSNPs = set([])
    for snp in snps:
        uniqueSNPs.add(getUniqueSNPTabix(snp, tb))
    return uniqueSNPs
    
def recurseToRootAddParents(clade, hier, tb):
    parent = getParentTabix(clade, tb)
    if parent != None:
        hier[clade] = parent
        if parent not in hier:
            recurseToRootAddParents(parent, hier, tb)

def createChildMap(hier):
    childMap = {}
    for child in hier:
        if hier[child] not in childMap:
            childMap[hier[child]] = [child]
        else:
            childMap[hier[child]].append(child)
    return childMap
    
def createMinimalTree(positives, tbSNPclades, tbCladeSNPs):
    clades = set([])
    for snp in positives:
        for clade in getSNPClades(snp, tbSNPclades):
            clades.add(clade)
    hier = {}
    for clade in clades:
        recurseToRootAddParents(clade, hier, tbCladeSNPs)
    return hier

def createMiminalTreePanelRoots(panelRoots, tbCladeSNPs):
    hier = {}
    for clade in panelRoots:
        recurseToRootAddParents(clade, hier, tbCladeSNPs)
    return hier

def createCladeSNPs(hierarchy, tb):
    cladeSNPs = {}
    for clade in hierarchy:
        if hierarchy[clade] not in hierarchy:
            cladeSNPs[hierarchy[clade]] = getCladeSNPs(hierarchy[clade], tb)
        cladeSNPs[clade] = getCladeSNPs(clade, tb)
    return cladeSNPs

def getTotalSequence(clade, hierarchy):
    sequence = [clade]
    thisClade = clade
    while thisClade in hierarchy:
        thisClade = hierarchy[thisClade]
        sequence.append(thisClade)
    return sequence[:-1]
    
def getScore(sequence, totalSequence):
    return float(len(sequence)) / len(totalSequence)

def printSolutions(solutions):
    for solution in solutions:
        print(" ".join(solution), getScore(solution))

def getConflicts(sequence, negatives, cladeSNPs):
    conflictingNegatives = []
    for hg in sequence:
        if any(snp in negatives for snp in cladeSNPs[hg]):
            conflictingNegativeSnps = ""
            for snp in cladeSNPs[hg]:
                if snp in negatives:
                    conflictingNegativeSnps += " " + snp
            conflictingNegatives.append(hg + " @" + conflictingNegativeSnps + ";")
    return conflictingNegatives

import numpy as np
def getPathScores(fullSequence, confirmed, negatives, positives, conflicts, cladeSNPs):
    scores = []
    for thing in fullSequence:
        if thing in confirmed:
            negs = len(negatives.intersection(set(cladeSNPs[thing])))
            poses = len(positives.intersection(set(cladeSNPs[thing])))
            toappend = 0
            if poses + negs > 0:
                toappend = float(poses) / (poses + negs)
            scores.append(toappend)
        else:
            if thing in conflicts:
                scores.append(0)
            else:
                scores.append(0.5)
    return scores

def isBasal(clade, negatives, positives, hierarchy, childMap, cladeSNPs):
    basal = False
    children = getChildren(clade, childMap)
    if len(children) > 0:
        basal = True
        for child in children:
            isNeg = len(negatives.intersection(set(cladeSNPs[child]))) > 0
            isPos = len(positives.intersection(set(cladeSNPs[child]))) > 0
            if isNeg and not isPos:
                basal = basal and True
    return basal        

def getWarningsConf(conflicts):
    messages =[]
    for conflict in conflicts:
        messages.append(" " + conflict)
    return messages

from operator import itemgetter
    
def getRankedSolutions(positives, negatives, hierarchy, childMap, cladeSNPs):
    solutions = []
    recurseDownTree(positives, hierarchy, childMap, cladeSNPs, solutions)
    scoredSolutions = []
    print(solutions)
    uniqueSolutions = removeDuplicates(solutions)
    print(uniqueSolutions)
    for solution in solutions:
        lastChainMoreNegThanPos = True
        removed = 0
        while lastChainMoreNegThanPos and removed < len(solution):
            totalSequence = getTotalSequence(solution[-1 - removed], hierarchy)
            totalSequence.reverse()
            conflicts = getConflicts(totalSequence, negatives, cladeSNPs)
            scores = getPathScores(totalSequence, solution, negatives, positives, conflicts, cladeSNPs)
            clade = solution[-1 - removed]
            if isBasal(clade, negatives, positives, hierarchy, childMap, cladeSNPs):
                clade = clade + "*"
            scoredSolutions.append([totalSequence, clade, np.average(scores), np.sum(scores), np.average(scores) * np.sum(scores), getWarningsConf(conflicts)])
            removed = removed + 1
            if scores[-1] > 0.5:
                lastChainMoreNegThanPos = False
            #else:
                #print(totalSequence, scores[-1], scores)
            
        #print(scoredSolutions[-1])
    scoredSolutions = sorted(scoredSolutions, key=itemgetter(4), reverse=True)
    
    return scoredSolutions

def removeDuplicates(arr): 

    n = len(arr)
    # Return, if array is  
    # empty or contains 
    # a single element 
    if n == 0 or n == 1: 
        return n 
  
    temp = list(range(n)) 
  
    # Start traversing elements 
    j = 0; 
    for i in range(0, n-1): 
  
        # If current element is 
        # not equal to next 
        # element then store that 
        # current element 
        if arr[i] != arr[i+1]: 
            temp[j] = arr[i] 
            j += 1
  
    # Store the last element 
    # as whether it is unique 
    # or repeated, it hasn't 
    # stored previously 
    temp[j] = arr[n-1] 
    j += 1
      
    # Modify original array 
    for i in range(0, j): 
        arr[i] = temp[i] 
  
    return arr

def getChildren(clade, childMap):
#    children = []
#    for child in childParents:
#        if childParents[child] == clade:
#            children.append(child)
#
    if clade in childMap:
        return childMap[clade]
    else:
        return []

def isInChildrenThisLevel(clade, positives, childMap, cladeSNPs):
    children = getChildren(clade, childMap)
    inChildren = []
    for child in children:
        if any(snp in positives for snp in cladeSNPs[child]):
            inChildren.append(child)
    return inChildren

def recurseDownTreeUntilFirstHits(clade, positives, childParents, childMap, cladeSNPs):
    posChildrenThisLevel = isInChildrenThisLevel(clade, positives, childMap, cladeSNPs)
    for child in getChildren(clade, childMap):
        if child not in posChildrenThisLevel:
            childResult = recurseDownTreeUntilFirstHits(child, positives, childParents, childMap, cladeSNPs)
            for cres in childResult:
                posChildrenThisLevel.append(cres)
    return posChildrenThisLevel

def refineHitsRecursively(sequences, positives, childParents, childMap, cladeSNPs, solutions):
    for sequence in sequences:
        refinedResults = recurseDownTreeUntilFirstHits(sequence[-1], positives, childParents, childMap, cladeSNPs)
        if len(refinedResults) == 0:
            solutions.append(sequence)
        else:
            print(sequence, refinedResults)
            for refRes in refinedResults:
                #print(sequence, refRes)
                seqCopy = sequence[:]
                seqCopy.append(refRes)
                refineHitsRecursively([seqCopy], positives, childParents, childMap, cladeSNPs, solutions)
                
def recurseDownTree(positives, childParents, childMap, cladeSNPs, solutions):
    sequences = recurseDownTreeUntilFirstHits("Adam", positives, childParents, childMap, cladeSNPs)
    newSequences = []
    for sequence in sequences:
        newSequences.append([sequence])
    refineHitsRecursively(newSequences, positives, childParents, childMap, cladeSNPs, solutions)

import json

def getPanels(snpPanelConfigFile):
    snpPanelsJson = json.load(open(snpPanelConfigFile))
    yfullCladePanels = {}
    for key in snpPanelsJson:
        branches = snpPanelsJson[key]["branches"]
        for branch in branches:
            yfullCladePanels[branch.replace("*","")] = snpPanelsJson[key]["html"]
    return yfullCladePanels

def getRankedSolutionsScratch(positives, negatives, tbCladeSNPs, tbSNPclades):
    hierarchy = createMinimalTree(positives, tbSNPclades, tbCladeSNPs)
    print(hierarchy)
    childMap = createChildMap(hierarchy)
    print(childMap)
    cladeSNPs = createCladeSNPs(hierarchy, tbCladeSNPs)
    print(cladeSNPs)
    b = getRankedSolutions(positives, negatives, hierarchy, childMap, cladeSNPs)
    return b

def getJSON(params, positives, negatives, tbCladeSNPsFile, tbSNPcladesFile):
    
    return json.dumps(getJSONObject(params, positives, negatives, tbCladeSNPsFile, tbSNPcladesFile))

def decorateJSONObject(params, clade, score, positives, negatives, tbCladeSNPs):
    theobj = {}
    theobj["clade"] = clade
    if "downstream" in params:
        theobj["downstream"] = getDownstreamSNPsJSONObject(clade, positives, negatives, tbCladeSNPs)
    if "phyloeq" in params:
        theobj["phyloeq"] = getCladeSNPStatusJSONObject(clade, positives, negatives, tbCladeSNPs)
    if "score" in params:
        theobj["score"] = score
    return theobj
    
def getJSONObject(params, positives, negatives, tbCladeSNPsFile, tbSNPcladesFile):
    tbSNPclades = tabix.open(tbSNPcladesFile)
    tbCladeSNPs = tabix.open(tbCladeSNPsFile)
    print(getUniqueSNPTabix(list(positives)[0], tbSNPclades))
    uniqPositives = getUniqueSNPsetTabix(positives, tbSNPclades)
    uniqNegatives = getUniqueSNPsetTabix(negatives, tbSNPclades)
    
    print("positives :" + ", ".join(list(uniqPositives)))
    print("negatives :" + ", ".join(list(uniqNegatives)))
    conflicting = uniqPositives.intersection(uniqNegatives)
    if len(conflicting) > 0:
        return {"error": "conflicting calls for same SNP with names " + ", ".join(list(conflicting))}
    ranked = getRankedSolutionsScratch(uniqPositives, uniqNegatives, tbCladeSNPs, tbSNPclades)
    if "all" in params:
        result = []
        for r in ranked:  
            clade = r[1]
            score = r[2]
            result.append(decorateJSONObject(params, clade, score, uniqPositives, uniqNegatives, tbCladeSNPs))
        return result
    else:
        if len(ranked) > 0:
            clade = ranked[0][1]
            score = ranked[0][2]
            return decorateJSONObject(params, clade, score, uniqPositives, uniqNegatives, tbCladeSNPs)
        else:
            return {"clade": "unable to determine"}        

def getCladeSNPStatusJSONObject(clade, positives, negatives, tbCladeSNPs):
    status = {}
    snps = getCladeSNPs(clade, tbCladeSNPs)
    poses = set(positives).intersection(snps)
    negs = set(negatives).intersection(snps)
    for snp in snps:
        if snp in poses:
            status[snp] = "+"
        elif snp in negs:
            status[snp] = "-"
        else:
            status[snp] = "?"
    return status

def getDownstreamSNPsJSONObject(clade, positives, negatives, tbCladeSNPs):
    children = getChildrenTabix(clade, tbCladeSNPs)
    snpStatus = {}
    for child in children:
        snpStatus[child] = getCladeSNPStatusJSONObject(child, positives, negatives, tbCladeSNPs)
    return snpStatus

def findCladeRefactored(positives, negatives, tbCladeSNPsFile, tbSNPcladesFile, snpPanelConfigFile):
    obj = getJSONObject("all,phyloeq,downstream,score", positives, negatives, tbCladeSNPsFile, tbSNPcladesFile)
    if len(obj) > 0:
        html = "<table><tr><td>Clade</td><td>Score</td></tr>"
        for res in obj:
            if "clade" in res:
                if res["clade"] != "unable to determine":
                    html = html + '<tr><td><a href="https://www.yfull.com/tree/' + res["clade"] + '">' + res["clade"] + "</a></td><td>" + str(round(res["score"],3)) + "</td></tr>"
                else:
                    html = html + '<tr><td>unable to determine</td><td></td></tr>'
        html = html + "</table>"
        panels = getPanels(snpPanelConfigFile)
        tbCladeSNPs = tabix.open(tbCladeSNPsFile)
        tbSNPclades = tabix.open(tbSNPcladesFile)
        panelRootHierarchy = createMiminalTreePanelRoots(panels, tbCladeSNPs)
        panelsDownstreamPrediction = []
        panelRootsUpstreamPrediction = []
        panelsEqualToPrediction = []
        
        uniqPositives = getUniqueSNPsetTabix(positives, tbSNPclades)
        uniqNegatives = getUniqueSNPsetTabix(negatives, tbSNPclades)
    
        hierarchy = createMinimalTree(positives, tbSNPclades, tbCladeSNPs)
        
        for panel in panels:
            if panel == obj[0]["clade"]:
                panelsEqualToPrediction.append(panel)
            else:
                if isUpstream(obj[0]["clade"],panel,hierarchy):
                    panelRootsUpstreamPrediction.append(panel)
                else:
                    if isDownstreamPredictionAndNotBelowNegative(obj[0]["clade"],panel,uniqNegatives,panelRootHierarchy,tbCladeSNPs):
                        panelsDownstreamPrediction.append(panel)
        def sortPanelRootsUpstream(panels, clade, hierarchy):
            thesorted = []
            for cld in getTotalSequence(clade, hierarchy):
                for panel in panels:
                    if panel == cld:
                        thesorted.append(panel)
            if len(thesorted) == 0:
                return []
            else:
                return [thesorted[0]]
                
        html = html + "<br><br><b>Recommended Panels</b><br><br>"
        count = 0
        for recommendedPanel in panelsEqualToPrediction:
            count = count + 1
            html = html + str(count) + ". " + panels[recommendedPanel] + "<br><br><i>Predicted " + obj[0]["clade"] + " is the panel root. This panel is applicable and will definitely provide higher resolution.</i><br><br>"
        
        if count == 0:
            for recommendedPanel in sortPanelRootsUpstream(panelRootsUpstreamPrediction, obj[0]["clade"], hierarchy):
                count = count + 1
                html = html + str(count) + ". " + panels[recommendedPanel] + "<br><br><i>Predicted " + obj[0]["clade"] + " is downstream of the panel root. This panel is applicable and may provide higher resolution to the extent that it tests subclades below " + obj[0]["clade"] + ".</i><br><br>"
            for recommendedPanel in panelsDownstreamPrediction:
                count = count + 1
                html = html + str(count) + ". " + panels[recommendedPanel] + "<br><br><i>Subject has not tested positive for root SNP. Absent a strong STR prediction for this clade, we recommend testing the root SNP before ordering this panel.</i><br><br>"

            #2nd Phase Development - get panel SNPs from API: html = html + "<br>" + getSNPpanelStats(b[0][1], panel, tbSNPclades, tbCladeSNPs) + "<br>"
        html = html + "<br><br>" + createSNPStatusHTML(obj[0]["clade"], uniqPositives, uniqNegatives, tbCladeSNPs)
    print(html)

    
def findClade(positives, negatives, tbCladeSNPsFile, tbSNPcladesFile, snpPanelConfigFile):
    tbSNPclades = tabix.open(tbSNPcladesFile)
    tbCladeSNPs = tabix.open(tbCladeSNPsFile)    
    hierarchy = createMinimalTree(positives, tbSNPclades, tbCladeSNPs)
    uniqPositives = getUniqueSNPsetTabix(positives, tbSNPclades)
    uniqNegatives = getUniqueSNPsetTabix(negatives, tbSNPclades)
    print(hierarchy)
    childMap = createChildMap(hierarchy)
    print(childMap)
    cladeSNPs = createCladeSNPs(hierarchy, tbCladeSNPs)
    print(cladeSNPs)
    b = getRankedSolutions(uniqPositives, uniqNegatives, hierarchy, childMap, cladeSNPs)
    html = "unable to determine clade"
    if len(b) > 0:
        html = "<table><tr><td>Clade</td><td>Score</td></tr>"
        for res in b:
            html = html + '<tr><td><a href="https://www.yfull.com/tree/' + res[1] + '">' + res[1] + "</a></td><td>" + str(round(res[2],3)) + "</td></tr>"
        html = html + "</table>"
        panels = getPanels(snpPanelConfigFile)
        panelRootHierarchy = createMiminalTreePanelRoots(panels, tbCladeSNPs)
        panelsDownstreamPrediction = []
        panelRootsUpstreamPrediction = []
        panelsEqualToPrediction = []
        
        
        for panel in panels:
            if panel == res[1]:
                panelsEqualToPrediction.append(panel)
            else:
                if isUpstream(res[1],panel,hierarchy):
                    panelRootsUpstreamPrediction.append(panel)
                else:
                    if isDownstreamPredictionAndNotBelowNegative(b[0][1],panel,uniqNegatives,panelRootHierarchy,tbCladeSNPs):
                        panelsDownstreamPrediction.append(panel)
        def sortPanelRootsUpstream(panels, clade, hierarchy):
            thesorted = []
            for cld in getTotalSequence(clade, hierarchy):
                for panel in panels:
                    if panel == cld:
                        thesorted.append(panel)
            if len(thesorted) == 0:
                return []
            else:
                return [thesorted[0]]
                
        html = html + "<br><br><b>Recommended Panels</b><br><br>"
        count = 0
        for recommendedPanel in panelsEqualToPrediction:
            count = count + 1
            html = html + str(count) + ". " + panels[recommendedPanel] + "<br><br><i>Predicted " + res[1] + " is the panel root. This panel is applicable and will definitely provide higher resolution.</i><br><br>"
        
        if count == 0:
            for recommendedPanel in sortPanelRootsUpstream(panelRootsUpstreamPrediction, res[1], hierarchy):
                count = count + 1
                html = html + str(count) + ". " + panels[recommendedPanel] + "<br><br><i>Predicted " + res[1] + " is downstream of the panel root. This panel is applicable and may provide higher resolution to the extent that it tests subclades below " + res[1] + ".</i><br><br>"
            for recommendedPanel in panelsDownstreamPrediction:
                count = count + 1
                html = html + str(count) + ". " + panels[recommendedPanel] + "<br><br><i>Subject has not tested positive for root SNP. Absent a strong STR prediction for this clade, we recommend testing the root SNP before ordering this panel.</i><br><br>"

            #2nd Phase Development - get panel SNPs from API: html = html + "<br>" + getSNPpanelStats(b[0][1], panel, tbSNPclades, tbCladeSNPs) + "<br>"
        html = html + "<br><br>" + createSNPStatusHTML(b[0][1], uniqPositives, uniqNegatives, tbCladeSNPs)
    print(html)

def isUpstream(predictedClade, panelRoot, hierarchyForClade):
    sequence = getTotalSequence(predictedClade, hierarchyForClade)
    passed = False
    for clade in sequence:
        if not passed:
            if clade == panelRoot:
                passed = True
    return passed

def isDownstreamPredictionAndNotBelowNegative(predictedClade, panelRoot, negatives, hierarchy, tbCladeSNPs):
    sequence = getTotalSequence(panelRoot, hierarchy)
    passed = False
    failed = False    
    for clade in sequence:
        if not failed and not passed:
            snps = set(getCladeSNPs(clade, tbCladeSNPs))
            intersects = len(snps.intersection(negatives))
            if intersects == 0:
                if predictedClade == clade:
                    passed = True
            else:
                failed = True
    return passed

def getSNPStatus(snp):
    return "Query YSEQ for ordering status of SNP"

def createSNPStatusHTML(clade, positives, negatives, tbCladeSNPs):
    children = getChildrenTabix(clade, tbCladeSNPs)
    snpStatus = {}
    for child in children:
        snps = getCladeSNPs(child, tbCladeSNPs)
        poses = set(positives).intersection(snps)
        negs = set(negatives).intersection(snps)
        status = "uncertain"
        if len(poses) > 0 and len(negs) > 0:
            status = "Split Result: " + ", ".join(poses) + " positive, " + ", ".join(negs) + " negative"
        else:
            if len(poses) > 0:
                status = "Positive due to " + ", ".join(poses) + " positive"
            else:
                if len(negs) > 0:
                    status = "Negative due to " + ", ".join(negs) + " negative"
                else:
                    status = getSNPStatus(child)
        snpStatus[child] = status
    if len(children) > 0:
        html = "<b>Downstream Lineages</b><br><br><table><tr><td>Clade</td><td>Status</td></tr>"
        for child in children:
            html = html + "<tr><td>" + child + "</td><td>" + snpStatus[child] + "</td></tr>"
        html = html + "</table>"
    else:
        html = "<b>No Downstream Lineages Yet Discovered</b>"
    return html

def getPanelSNPs(panel):
    return ["M241","L283","Z2432","Z1297","Z1295","CTS15058","CTS6190","Z631","Z1043","Y87609","PH1553","Y26712", "Y32998", "Y29720","Z8424","Y98609","M102"]   

def getCladesFromSNPpanel(snps, panel, tbSNPclades):
    clades = []
    unknownPanelSNPs = []
    for snp in snps:
        theclades = getSNPClades(snp, tbSNPclades)
        if len(theclades) == 1:
            clades.append(theclades[0])
        else:
            if len(theclades) > 1:
                for clade in theclades:
                    if clade[0] == panel[0]:                        
                        clades.append(clade)
            else:
                unknownPanelSNPs.append(snp)
    return clades

def recurseDownCladeWithinPanel(clade, childMap, panelClades, possible):
    if clade in childMap:
        for child in childMap[clade]:
            recurseDownCladeWithinPanel(child, childMap, panelClades, possible)
    if clade in panelClades:
        possible.append(clade)
    
def getSNPpanelStats(predictedClade, panelRootClade, tbSNPclades, tbCladeSNPs):
    panelSNPs = getPanelSNPs(panelRootClade)
    panelClades = getCladesFromSNPpanel(panelSNPs, panelRootClade, tbSNPclades)
    
    hier = {}
    for clade in panelClades:
        recurseToRootAddParents(clade, hier, tbCladeSNPs)

    childMap = createChildMap(hier)
    
    panelPositiveClades = []
    
    curr = predictedClade
    
    while curr in hier and curr != panelRootClade:
        if curr in panelClades:
            panelPositiveClades.append(curr)
        curr = hier[curr]
    
    if curr == panelRootClade:
        panelPositiveClades.append(curr)
        
    possibleRemaining = []
    
    recurseDownCladeWithinPanel(predictedClade, childMap, panelClades, possibleRemaining)
    if predictedClade in possibleRemaining:
        possibleRemaining.remove(predictedClade)
    
    
    #maximumTestsToTerminalSubclade = None
    #meanTestsToTerminalSubcladeGivenNoAprioris = None
    #expectedTestsToTerminalSubcladeGivenYFullAprioris = None
    return "PH1553 clades: " + str(getCladeSNPs("PH1553",tbCladeSNPs)) + ", panelClades: " + str(panelClades) + ", total positive: " + str(panelPositiveClades) + ", possible remaining: " + str(possibleRemaining)
    
#def isDownstreamPredictionAndNotBelowNegative(predictedClade, panelRoot, negatives, childMap, tbCladeSNPs):
#    children = getChildren(predictedClade, childMap)
#    passes = False
#    for child in children:
#        snps = set(getCladeSNPs(child, tbCladeSNPs))
#        intersects = len(snps.intersection(negatives))
#        if intersects == 0:
#            passes = passes or isDownstreamPredictionAndNotBelowNegative(child, panelRoot, negatives, childMap, tbCladeSNPs)
#            
#        
#def recommendPanel(prediction, positives, negatives):
#    allpanels = {}
#    for panel in allpanels:
        
