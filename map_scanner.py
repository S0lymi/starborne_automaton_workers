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
      print("Tesseract probably not in PATH, write path to .exe below (Hint: It's probably C:\Program Files\Tesseract-OCR\\tesseract.exe)")
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


#to parse text of hexes
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
    

time.sleep(wait_durations[0])

#get in position ( dragdoesnt work for some reason)
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
preloaded = False #To keep track of preloaded hexes
coordlist = traverse_hexes(int(middlecoords[0]),int(middlecoords[1]),int(scanradius))
random.Random(42).shuffle(coordlist) #so checking with strdist can make sense later
for index_num in range(resume_index,len(coordlist)):
    readlocation = 677,131
    coords = coordlist[index_num]
    failcounter = 0
    while True: #try until coordinate is successfully read(passes end check)
        if not preloaded:
            pyautogui.click(x=45, y=1042, button='left')
            pyautogui.typewrite('/goto ' + repr(coords[0])+' '+ repr(coords[1]) + '\n', interval=wait_durations[3])
            pyautogui.moveTo(readlocation, duration=wait_durations[2])
        else:
            preloaded = False #reset preload
        
        
        time.sleep(wait_durations[1])
        
        popup_read_fail = 0
        while True: #wait for orange to pop up if needed
            xborder= 0
            yborder = 0
            readlocation=pyautogui.position()
            im = pyautogui.screenshot(region=(readlocation[0]+25,readlocation[1]+25, readwindow[0], readwindow[1]))
            if popup_read_fail > 30: # if at least 1.5s passed randomly move mouse to combat starborne's graphical bugs
                pyautogui.moveTo((readlocation[0] + random.randrange(-20,20,1),readlocation[1] + random.randrange(-20,20,1)), duration=wait_durations[2]+0.05)
            
            for xy in range(im.size[1]-11):
                if xborder !=0:
                    break
                for x in range(im.size[0]):
                    if im.getpixel((x,xy)) == bordercolor:
                        borderfound = True
                        for y in range(11):
                            borderfound = borderfound and im.getpixel((x,y+xy)) == bordercolor
                        if borderfound == True:
                            xborder = x
                            break
            for yx in range(im.size[0]):
                if yborder != 0:
                    break
                for y in range(im.size[1]-10):
                    if im.getpixel((yx,y)) == bordercolor:
                        borderfound = True
                        for x in range(10):
                            borderfound = borderfound and im.getpixel((x+yx,y)) == bordercolor
                        if borderfound == True:
                            yborder = y
                            break
            
            #print(xborder,yborder)
            if xborder == 0 or yborder == 0:
                time.sleep(0.05)
                popup_read_fail = popup_read_fail + 1
            else:
                break
            
        #maybe speedup if we go to next coordinate while processing image?
        if index_num+1 < len(coordlist):
            nextcoords= coordlist[index_num+1]
            pyautogui.click(x=45, y=1042, button='left')
            pyautogui.typewrite('/goto ' + repr(nextcoords[0])+' '+ repr(nextcoords[1]) + '\n', interval=wait_durations[3])
            readlocation = 677,131
            pyautogui.moveTo(readlocation, duration=wait_durations[2])
            preloaded = True
            
        imtop = im.crop((0,5,xborder- 3, 33))
        #imbottom = im.crop((0 ,yborder-29, xborder- 3, yborder-16))
        
        imbottom = im.crop((0, yborder-35, xborder- 3, yborder-10))
        
        #poke the neural net with a slightly different image if it gets stuck (actually seems better as default too)
        if failcounter < 4:
            imbottom.paste(imbottom.crop((6,0,10,imbottom.size[1])),(11,0))
            #imbottom.show()
        
        deviant=False
        #get strings from image
        topstr=pytesseract.image_to_string(ImageOps.invert(imtop)) #invert need for tesseract to work properly
        bottomstr=pytesseract.image_to_string(ImageOps.invert(imbottom)) #,config='outputbase digits')
        #pytesseract.image_to_string(someimage, config='outputbase digits')
        
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
        namestr=cellnamelist[distances.index(min(distances))]
        if min(distances) > 1:
            deviant = True
            
        #parse owner and claim
        ownerpos = topstr.find('Owner')
        if ownerpos != -1:
            ownerstr = topstr[ownerpos+7:topstr.rfind('(')]
        else:
            ownerstr = ""
        
        claimpos = topstr.rfind('(')+1
        if claimpos != 0:
            claimstr = topstr[topstr.rfind('(')+1:topstr.rfind(')')]
        else:
           claimstr = ""
        #print parsed
        print('parsed: '+coordsstr+','+namestr+','+claimstr+','+ownerstr)
        print('checkcoords:'+ str(coords[0])+','+str(coords[1]))
        
        
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
        preloaded = False #reload advised
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
        failcounter = failcounter+1
    
    f = open("map.txt", "a")
    f.write(str(coords[0])+','+str(coords[1])+','+namestr+','+claimstr+','+ownerstr+'\n')
    f.close()
    
    

