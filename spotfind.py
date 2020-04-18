# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 00:27:58 2020

@author: Solymi
"""

"""
import json
json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
"""


import json
mapfile="map_checked.txt"
cell_json= "CELL_DEFINITIONS.json"
#some classes to look nice
class Hex:
    def __init__(self, x=0, y=0,name="",claim =0, owner = ""):
        self.x = x
        self.y = y
        self.name = name
        self.claim = claim
        self.owner = owner
    
class Hexmap:
    def __init__(self,x=1000,y=1000):
        self.hexarray = [[Hex()] * x for i in range(y)]
        self.xsize=x
        self.ysize=y
    
    def get(self, x, y):
        return self.hexarray[int(x+self.xsize/2)][int(y+self.ysize/2)]
    def set(self, x, y, sethex):
        self.hexarray[int(x+self.xsize/2)][int(y+self.ysize/2)] = sethex

#load json
file = open(cell_json,'r')
#because magic
test = file.read()
file.close()
test = test[test.find('['):]
cellinfo = json.loads(test)
#magic end

#load map
hmap = Hexmap()
with open(mapfile) as file:
    for line in file: 
        line = line.strip()
        parsetuple= tuple(line.split(','))
        try:
            parseclaim = str(int(parsetuple[3]))
        except ValueError:
            parseclaim = 0
        #hmap.set(int(parsetuple[0]),int(parsetuple[1]),Hex(int(parsetuple[0]),int(parsetuple[1]),parsetuple[2],int(parsetuple[3]),parsetuple[4]))
        parsedhex = Hex(int(parsetuple[0]), int(parsetuple[1]), parsetuple[2], parseclaim, parsetuple[4])
        hmap.set(int(parsetuple[0]),int(parsetuple[1]),parsedhex)
        

#define

def traverse_hexes(x = 0, y = 0, radius = 500):
    traverse_list = []
    for ix in range(-radius,radius+1):
        if ix >=0:
            for iy in range(-radius,radius-ix+1):
                traverse_list.append((ix+x,iy+y))
        else:
            for iy in range(-radius-ix,radius+1):
                traverse_list.append((ix+x,iy+y))
    return traverse_list

def eval_MC(x,y, radius = 1, maxclaim = 200):
    hexlist=traverse_hexes(x,y,radius)
    value = 0
    #check if the spot is free
    if hmap.get(x,y).name != "":
        return value
    #iterate over surroundings
    for h in hexlist:
        if int(hmap.get(h[0],h[1]).claim) <= maxclaim: #check if its claimable
            match = [x for x in cellinfo if x["Name"] == hmap.get(h[0],h[1]).name] #match name
            if len(match) > 0:
                if match[0]["Type"] == 1: #its a planet
                    value = value + match[0]["HarvestValue"]["CR"] + match[0]["HarvestValue"]["GR"] + match[0]["HarvestValue"]["MR"]
                if match[0]["Type"] == 2: #its a field
                    value = value + 0.5 * (match[0]["HarvestValue"]["CR"] + match[0]["HarvestValue"]["GR"] + match[0]["HarvestValue"]["MR"])
    return value
    
#sample search
search_middle = 70, -234
search_radius = 50
spot_radius = 3
maxclaim = 300
value_threshold = 20 * 24
eval_function = eval_MC

hlist = traverse_hexes(search_middle[0],search_middle[1],search_radius)
result = []

for h in hlist:
    value = eval_function(h[0],h[1],spot_radius,maxclaim)
    if value >= value_threshold:
        result.append((h,value))
#sort
result.sort(key=lambda tup: tup[1], reverse=True)
#print nicely
for res in result:
    print("Value: "+str(res[1]/24)+" at: /goto "+ str(res[0][0])+' '+ str(res[0][1]))



