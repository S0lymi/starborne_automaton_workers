# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 16:26:17 2020

@author: Solymi
"""

import pyautogui
import time
from PIL import ImageOps, Image, ImageDraw
import pytesseract
from Levenshtein import distance as strdist
import random
import os

if not os.path.exists('deviants'):
    os.makedirs('deviants')
    
print('Starborne manual labor automaton workers for scanning the map.')
print('(Map The Stars fo Starborne)')
while True:
    try:
      print(pytesseract.image_to_string('tesseract_test.png', timeout=2))
      break
    except:
      print("Tesseract probably not in PATH, write path to .exe below (Hint: It's probably C:\Program Files\Tesseract-OCR\tesseract.exe)")
      tesspath = input('Tesseract path:')
      pytesseract.pytesseract.tesseract_cmd = tesspath
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
      


print('Input delays in seconds (these can be 0 of course), separator is (space)')
wait_durations = tuple(input("Delays: initial,gui,mouse,typing: ").split(' '))
print(wait_durations)
if len(wait_durations) != 4:
    print("Wrong format, going with 10 second initial, rest 0s.")
    wait_durations = 10, 0, 0, 0  
scaninput= list(input("Give middle coordinates and radius (x y radius): ").split(' '))
middlecoords = scaninput[0:2]
scanradius = scaninput[2]
resume_index = int(input("Start index:" ))
savedeviants = bool(int(input("Save pics of all the deviant ones? (0 or 1 ): ")))
print('ALT+TAB and HANDS UP')


readlocation = 677,131
readwindow = 500, 550
bordercolor = 254, 87,35 #RGB for that nice orange
#coords = 79, -247
"""
middlecoords = 79, -247
scanradius = 2
wait_durations = 10, 0, 0, 0
savedeviants = True
"""

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



cellnamelist = ["Terrestrial Planet","Grand Terrestrial Planet",
                "Desert Planet","Grand Desert Planet",
                "Ocean Planet","Grand Ocean Planet",
                "Barren Planet","Grand Barren Planet",
                "Gas Planet","Grand Gas Planet"
                "Ice Planet","Grand Ice Planet",
                "Jungle Planet","Grand Jungle Planet",
                "Lava Planet","Grand Lava Planet",
                "Plasma Planet","Grand Plasma Planet",
                "Barren Planet","Grand Barren Planet",
                "Small Ice Field","Medium Ice Field","Large Ice Field",
                "Small Metal Field","Medium Metal Field","Large Metal Field",
                "Small Gas Field","Medium Gas Field","Large Gas Field",
                "Small Crystal Field","Medium Crystal Field","Large Crystal Field",
                "Small Rock Moon","Rock Moon","Large Rock Moon",
                "Small Misty Moon","Misty Moon","Large Misty Moon",
                "Small Frozen Moon","Frozen Moon","Large Frozen Moon",
                "Small Iron Moon","Iron Moon","Large Iron Moon",
                "Small Volcanic Moon","Volcanic Moon","Large Volcanic Moon",
                "Small Atmospheric Moon","Atmospheric Moon","Large Atmospheric Moon",
                "White Dwarf","Brown Dwarf","Red Dwarf","Red Star","Yellow Star","Blue Star",
                "Blue Giant","Blue Supergiant","Red Supergiant","Black Hole",
                "Mysterious Mechanism","Enigmatic Mechanism","Broken Planet",
                "Vortex","Debris","Large Debris",""]
    
"""
#load images into list
topimlist = []
numberimlist = []
bottomimlist = []

for i in range(10):
    imload = Image.open('res/'+repr(i)+'.png')
    numberimlist.append(imload)
"""

time.sleep(wait_durations[0])

#get in position (doesnt work for some reason)
"""
screenWidth, screenHeight = pyautogui.size()
pyautogui.moveTo(screenWidth/2, screenHeight/2+100, 2)
pyautogui.mouseDown(button='right')
time.sleep(0.2)
pyautogui.moveTo(screenWidth/2, screenHeight, 1.5)
pyautogui.mouseUp(button='right')
pyautogui.scroll(10)
"""

#print(screenWidth, screenHeight)
#print(currentMouseX,currentMouseY)
coordlist = traverse_hexes(int(middlecoords[0]),int(middlecoords[1]),int(scanradius))
random.Random(42).shuffle(coordlist) #so checking with strdist can make sense later
for index_num in range(resume_index,len(coordlist)):
    coords = coordlist[index_num]
    failcounter = 0
    while True: #try until coordinate is successfully read(passes end check)
        pyautogui.click(x=45, y=1042, button='left')
        pyautogui.typewrite('/goto ' + repr(coords[0])+' '+ repr(coords[1]) + '\n', interval=wait_durations[3])
        pyautogui.moveTo(readlocation, duration=wait_durations[2])
        
        
        time.sleep(wait_durations[1])
        while True: #wait for orange to pop up if needed
            xborder= 0
            yborder = 0
            im = pyautogui.screenshot(region=(readlocation[0]+25,readlocation[1]+25, readwindow[0], readwindow[1]))
            for x in range(im.size[0]):
                if im.getpixel((x,0)) == bordercolor:
                    borderfound = True
                    for y in range(20):
                        borderfound = borderfound and im.getpixel((x,y)) == bordercolor
                    if borderfound == True:
                        xborder = x
                        break
                    
            for y in range(im.size[1]):
                if im.getpixel((0,y)) == bordercolor:
                    borderfound = True
                    for x in range(20):
                        borderfound = borderfound and im.getpixel((x,y)) == bordercolor
                    if borderfound == True:
                        yborder = y
                        break
            
            #print(xborder,yborder)
            if xborder == 0:
                time.sleep(wait_durations[2])
            else:
                break
        imtop = im.crop((0,5,xborder- 3, 33))
        #imbottom = im.crop((0 ,yborder-29, xborder- 3, yborder-16))
        
        imbottom = im.crop((0, yborder-35, xborder- 3, yborder-10))
        
        #poke the neural net with a slightly different image if it gets stuck (actually seems better as default too)
        if failcounter < 2:
            imbottom.paste(imbottom.crop((6,0,10,imbottom.size[1])),(11,0))
            #imbottom.show()
        
        deviant=False
        #get strings from image
        topstr=pytesseract.image_to_string(ImageOps.invert(imtop)) #invert need for tesseract to work properly
        bottomstr=pytesseract.image_to_string(ImageOps.invert(imbottom))
        
        print('top:'+topstr)
        print('bottom:'+bottomstr)
        #parse strings
        endindex = bottomstr.find(']')
        if endindex == -1:
            endindex = bottomstr.find(')') #in case ']' is mistaken for ')'
        coordsstr=bottomstr[bottomstr.find('[')+1:endindex]
        
        #parse name
        namestr = bottomstr[endindex+2:]
        distances=[]
        for cellname in cellnamelist:
            distances.append(strdist(namestr,cellname))
        if min(distances) < 2:
            namestr=cellnamelist[distances.index(min(distances))]
        else:
            deviant = True
            
    
        ownerstr = topstr[topstr.find('Owner')+7:topstr.rfind('(')]
        claimstr = topstr[topstr.rfind('(')+1:topstr.rfind(')')]
        #print parsed
        print('parsed: '+coordsstr+','+namestr+','+claimstr+','+ownerstr)
        print('checkcoords:'+ str(coords[0])+','+str(coords[1]))
        
        #im.show()
        #imtop.show()
        #ImageOps.invert(imtop).show()
        #imbottom.show()
        #ImageOps.invert(imbottom).show()
        #print('top: '+topstr)
        #print('bottom: '+bottomstr)
        #print(strdist(coordsstr,str(coords[0])+','+str(coords[1])))
        
        if strdist(coordsstr,str(coords[0])+','+str(coords[1])) < 2:
            if strdist(coordsstr,str(coords[0])+','+str(coords[1])) > 0:
                deviant=True
            if deviant and savedeviants:
                ownerstr = ownerstr + ', deviant'
                saveim = Image.new('RGB', (im.size[0], im.size[1]+imtop.size[1]+imbottom.size[1]+56))
                saveim.paste(im,(0,0))
                saveim.paste(ImageOps.invert(imtop),(0,im.size[1]))
                saveim.paste(ImageOps.invert(imbottom),(0,im.size[1]+imtop.size[1]+1))
                #The abomination
                ImageDraw.Draw(saveim).text((0,im.size[1]+imtop.size[1]+1+imbottom.size[1]),"top:"+topstr+"\n"+"bottom:"+bottomstr+"\n"+"parsed: "+coordsstr+","+namestr+","+claimstr+","+ownerstr+"\n"+"corrected: "+ str(coords[0])+","+str(coords[1])+","+namestr+","+claimstr+","+ownerstr+"\n")
                saveim.save('deviants/'+str(coords[0])+'_'+str(coords[1])+'_'+namestr+'.png')               
            print('corrected: '+ str(coords[0])+','+str(coords[1])+','+namestr+','+claimstr+','+ownerstr+'\n')
            print('PASS ('+str(index_num+1)+' of '+str(len(coordlist))+')\n')
            break
        print('CHECK FAIL: '+'checkcoords:'+ str(coords[0])+','+str(coords[1]))
        failcounter = failcounter+1
        if failcounter > 5:
            #save an image
            saveim = Image.new('RGB', (im.size[0], im.size[1]+imtop.size[1]+imbottom.size[1]+56))
            saveim.paste(im,(0,0))
            saveim.paste(ImageOps.invert(imtop),(0,im.size[1]))
            saveim.paste(ImageOps.invert(imbottom),(0,im.size[1]+imtop.size[1]+1))
            #The abomination again
            ImageDraw.Draw(saveim).text((0,im.size[1]+imtop.size[1]+1+imbottom.size[1]),"top:"+topstr+"\n"+"bottom:"+bottomstr+"\n"+"parsed: "+coordsstr+","+namestr+","+claimstr+","+ownerstr+"\n"+"corrected: "+ str(coords[0])+","+str(coords[1])+","+namestr+","+claimstr+","+ownerstr+"\n")
            saveim.save('deviants/!manual_'+str(coords[0])+'_'+str(coords[1])+'_'+namestr+'.png')
            ownerstr = ownerstr + ', MANUAL_LABOR'
            break
            
    
    f = open("map.txt", "a")
    f.write(str(coords[0])+','+str(coords[1])+','+namestr+','+claimstr+','+ownerstr+'\n')
    f.close()
"""    
    saveim = Image.new('RGB', (im.size[0], im.size[1]+imtop.size[1]+imbottom.size[1]+1))
    saveim.paste(im,(0,0))
    saveim.paste(ImageOps.invert(imtop),(0,im.size[1]))
    saveim.paste(ImageOps.invert(imbottom),(0,im.size[1]+imtop.size[1]+1))
    saveim.save('deviants/'+str(coords[0])+'_'+str(coords[1])+'.png')
"""
"""
im.show()
imtop.show()
imbottom.show()
ImageOps.invert(imbottom).show()
imtop.save("res/top.png")
imbottom.save("res/bottom.png")
"""
"""
for x in range(3):
    print(x)
    pyautogui.moveTo(500, 500, duration=0.2)
    pyautogui.moveTo(1500, 500, duration=0.2)
    pyautogui.moveTo(1500, 1000, duration=0.2)
    pyautogui.moveTo(500, 1000, duration=0.2)
"""    
