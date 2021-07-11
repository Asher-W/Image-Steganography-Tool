from tkinter import Tk, Frame, Label, Entry, Button, BOTH
from PIL import Image
from requests import get
from time import sleep
from math import ceil
from io import BytesIO

def process():
    URL, text, name = URLInput.get(), TextInput.get(), NameInput.get()
    
    encode_message(name, text, URL)

def encode_message(name, text, URL):
    request = get(URL)
    if request.status_code != 200:
        print("Connection Issue, error code: {}".format(request.status_code))
        return
    im = Image.open(BytesIO(request.content))
    fname = "x:/VSCode/code/" + name + ".png"
    width, height = im.size

    data = list(im.getdata())
    pixels = im.load()
    
    encoded = [[0,0],[0,1],[0,3]]
    baseRed = 0
    baseGreen = 0
    baseBlue = 0
    for index in range(len(URL)):
        if not index: seed = stringToNum(fname.split('/')[-1]) + 1
        else: seed = ord(URL[index - 1]) + index * 2
        posChange = 1
        while 1:
            newPix = [getSudoRandom(seed * width, 0, width), getSudoRandom((seed + height/2) * height, 0, height)]
            if newPix not in encoded: break
            seed = getSudoRandom(seed, 0, width) + posChange
            posChange += 1
        encoded.append(newPix)
        baseRed += data[encoded[-1][0] + (encoded[-1][1] * width)][0]
        baseGreen += data[encoded[-1][0] + (encoded[-1][1] * width)][1]
        baseBlue += data[encoded[-1][0] + (encoded[-1][1] * width)][2]

    baseRed = max(int(baseRed / len(encoded)), 65)
    baseGreen = max(int(baseRed / len(encoded)), 65)
    baseBlue =  max(int(baseBlue / len(encoded)), 65)

    pixels[0,0] = (baseRed, baseGreen, baseBlue)

    URLLen = len(URL)
    URL1 = ceil(URLLen / 3)
    if baseRed > 128: URL1 *= -1
    URLLen -= ceil(URLLen / 3)
    URL2 = ceil(URLLen / 2)
    if baseGreen > 128: URL2 *= -1
    URLLen -= ceil(URLLen / 2)
    URL3 = ceil(URLLen)
    if baseBlue > 128: URL3 *= -1
    pixels[0,1] = (baseRed + URL1, baseGreen + URL2, baseBlue + URL3)

    for index, point in enumerate(encoded[3:]):
        letterVal = ord(URL[index])
        Red = ceil(letterVal/3)
        if baseRed > 128: Red *= -1
        letterVal -= ceil(letterVal/3)
        Green = ceil(letterVal / 2)
        if baseGreen > 128: Green *= -1
        letterVal -= ceil(letterVal / 2)
        Blue = ceil(letterVal)
        if baseBlue > 128: Blue *= -1
        pixels[point[0], point[1]] = (baseRed + Red, baseGreen + Green, baseBlue + Blue)
    
    for i, v in enumerate(text):
        if not i: seed = ord(URL[-1]) + 1
        else: seed = ord(text[i - 1]) + index * 2
        posChange = 1
        while 1:
            newPix = [getSudoRandom(seed * width, 0, width), getSudoRandom((seed + height/2) * height, 0, height)]
            if newPix not in encoded: break
            seed = getSudoRandom(seed, 0, width) + posChange
            posChange += 1
        encoded.append(newPix)
        letterVal = max(ord(v), 1)
        colors = pixels[newPix[0], newPix[1]]
        Red = ceil(letterVal/3)
        if colors[0] > 128: Red *= -1
        letterVal -= ceil(letterVal/3)
        Green = ceil(letterVal / 2)
        if colors[1] > 128: Green *= -1
        letterVal -= ceil(letterVal / 2)
        Blue = ceil(letterVal)

        if colors[2] > 128: Blue *= -1
        pixels[newPix[0], newPix[1]] = (colors[0] + Red, colors[1] + Green, colors[2] + Blue)
    im.save(fname)
    im.close()

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

#create the object to hold widgets
root = Tk()
#edit geometry of the window
root.geometry("500x500")
root.resizable(0,0)

#whole storage area
mainFrame = Frame(root)

#take image details
URLLabel = Label(mainFrame, text="Image URL")
URLInput = Entry(mainFrame)

#take image details
NameLabel = Label(mainFrame, text="Image file Name (always a png)")
NameInput = Entry(mainFrame)

#take text details
TextLabel = Label(mainFrame, text="Encoded text")
TextInput = Entry(mainFrame)

#show widgets (using pack)
mainFrame.pack(expand=1,fill=BOTH, padx = 10, pady = 10)

URLLabel.pack()
URLInput.pack()
NameLabel.pack()
NameInput.pack()

TextLabel.pack()
TextInput.pack()

#submit button
Button(mainFrame, command = process, text = "process").pack()

#show the window and widgets
root.mainloop()

#https://sargeant.rcsdk8.org/sites/main/files/main-images/camera_lense_0.jpeg