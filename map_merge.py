# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 19:18:13 2020

@author: Solymi

"The quick stackoverflow copypasta"
"""

mergeinput= list(input("input files (tomerge1 tomerge2 destination_file): ").split(' '))

storedlines = []
with open(mergeinput[0]) as file:
    for line in file: 
        line = line.strip()
        storedlines.append(line)
print("read in")
        
with open(mergeinput[1]) as file:
    for line in file:
        line = line.strip() #preprocess line
        match = [storedlines.index(s) for s in storedlines if line in s]
        if len(match) > 0:
            linepriority = 0
            if "deviant" in line: linepriority = 1
            if "deviantTrue" in line: linepriority = 2
            if "MANUAL_LABOR" in line: linepriority = 3
            storedpriority = 0
            if "deviant" in storedlines[match[0]]: storedpriority = 1
            if "deviantTrue" in storedlines[match[0]]: storedpriority = 2
            if "MANUAL_LABOR" in storedlines[match[0]]: storedpriority = 3
            
            if storedpriority > linepriority:
                storedlines[match[0]] = line
        else:
            storedlines.append(line)
print("merged")
with open(mergeinput[2], 'w') as file:
    for line in storedlines:
        file.write(line+'\n')