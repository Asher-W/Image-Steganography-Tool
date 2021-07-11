from tkinter import Tk, Frame, Label, Entry, Button, filedialog, BOTH, StringVar
from PIL import Image
from requests import get
from io import BytesIO

import requests

def getMessage(file):
    im = Image.open(file)
    width, height = im.size

    pixels = im.load()
    baseColor = pixels[0,0]
    encodedLen = pixels[0,1]

    URLLength = (abs(baseColor[0] - encodedLen[0]) + abs(baseColor[1] - encodedLen[1]) + 
      abs(baseColor[2] - encodedLen[2]))
    encoded = [[0,0],[0,1]]
    savedURL = ""
    for index in range(URLLength):
        if not index: seed = stringToNum("Image.png") + 1
        else: seed = ord(savedURL[-1]) + index * 2
        posChange = 1
        while 1:
            newPix = [getSudoRandom(seed * width, 0, width), getSudoRandom((seed + height/2) * height, 0, height)]
            if newPix not in encoded: break
            seed = getSudoRandom(seed, 0, width) + posChange
            posChange += 1
        encoded.append(newPix)
        pixelColor = pixels[newPix[0],newPix[1]]
        savedURL = savedURL + chr(abs(baseColor[0] - pixelColor[0]) + abs(baseColor[1] - pixelColor[1]) + 
          abs(baseColor[2] - pixelColor[2]))
    request = get(savedURL)
    if request.status_code != 200:
        print("Connection Issue, error code: {}".format(request.status_code))
        return
    unEdit = Image.open(BytesIO(request.content))
    unEditPix = unEdit.load()
    i = 0
    savedText = ""
    while 1:
        if not i: seed = ord(savedURL[-1]) + 1
        else: seed = ord(savedText[i - 1]) + index * 2
        posChange = 1
        while 1:
            newPix = [getSudoRandom(seed * width, 0, width), getSudoRandom((seed + height/2) * height, 0, height)]
            if newPix not in encoded: break
            seed = getSudoRandom(seed, 0, width) + posChange
            posChange += 1
        encoded.append(newPix)
        unEditColor = unEditPix[newPix[0], newPix[1]]
        Color = pixels[newPix[0], newPix[1]]
        if unEditColor == Color: break
        savedText = savedText + chr(abs(Color[0] - unEditColor[0]) + abs(Color[1] - unEditColor[1]) + 
          abs(Color[2] - unEditColor[2]))
        i += 1
    del i

    TextOutput["text"] = savedText

def stringToNum(str : str):
    total = 0
    for i in range(len(str)): total += ord(str[i][0])
    return total

def getSudoRandom(seed, base, top):
    seed, base, top = int(seed), int(base), int(top)
    seedBin = bin(seed)[2:]
    endBin = bin(top)[2:]
    extraZeros = len(seedBin) - len(endBin)
    if extraZeros > 0:
        for i in range(0, extraZeros, 1): endBin = "0" + endBin
    if extraZeros < 0:
        for i in range(0, extraZeros, -1): seedBin = "0" + seedBin
    returnNum = ""
    for i in range(len(endBin)):
        if seedBin[i] == endBin[i]: returnNum = returnNum + "0"
        else: returnNum = returnNum + "1"
    num = 0
    for i, v in enumerate(returnNum):
        num += int(v) * 2 ** i
    returnNum = num
    del num

    return min(max(((returnNum ** 3 + base) ** 2 % (top - base)) + base, base), top - 1)

def select_file():
    file = filedialog.askopenfilename(initialdir= "/")
    getMessage(file)
#create the object to hold widgets
root = Tk()
#edit geometry of the window
root.geometry("500x500")
root.resizable(0,0)

#whole storage area
mainFrame = Frame(root)

#find the image
file_select = Button(mainFrame, command = select_file, text = "file")

#take text details
TextLabel = Label(mainFrame, text="Encoded text")
TextOutput = Label(mainFrame, text = "no file selected")

#show widgets (using pack)
mainFrame.pack(expand=1,fill=BOTH, padx = 10, pady = 10)

file_select.pack()

TextLabel.pack()
TextOutput.pack()

#show the window and widgets
root.mainloop()