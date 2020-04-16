# starborne_automaton_workers  

map_scanner.py is the actual map scanner.  

dependencies:  
-pyautogui https://pypi.org/project/PyAutoGUI/  
-pytesseract https://pypi.org/project/pytesseract/  
  It also needs the original Tesseract engine for it to work: https://tesseract-ocr.github.io/tessdoc/Home.html
  
## Use  

Run **map_scanner.py**. It uses Tesseract, so you'll need that istalled too (see dependencies). If tesseract.exe is not part of your PATH, tell them script it's location when it asks for it.
Parameters:  
 - Delays: initial: How many seconds to wait before script starts (time for you to ALT+TAB into starborne and setup the camera)  
           gui,mouse,typing: these are delays for mouse movements, time between keypresses, waiting for gui. (0 is fine for them, so use bigger if you better want to see whats going on).  
           Separator betwwen values is (whitespace). If format is not ok it defaults to 10 0 0 0 (my preferred settings)  
 -  coordinates: x y radius. x and y specifies a hex on the map radius specifies a radius (in hexes) around this middlepont. Hees in this radius will be scanned  
 - startindex: traversal my seem random, but its not, just shufled with a constant seed (cause reasons), so if you know what index you left off last time this can be used to continue an already started session. (The constant seed is hardcoded so its the same for everyone).  
 - deviants: Option to save picture of cases where the match wasn't exact. Pics are save with the nam x_y.png  
 When recognition falls below a crtain threshold files with names starting !manual keywords are created indicating that confidence in these cases are low and should be looked at manually if possible.  
 
Map is created as map.txt, output format is: x,y,name,claimstrength,owner
 
 ### Needed camera options
 When going back to game set the camera to vertically look down (perpendicular to that map plane), and zoom in as much as possible. This way when jumping with /goto-s the mouse is always in the correct hex.
