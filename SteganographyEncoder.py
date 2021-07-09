from tkinter import Tk, Frame, Label, Entry, Button, BOTH
from PIL import Image
from requests import get
from time import sleep
from random import randint, seed
from math import ceil, sqrt
import shutil
import os
from random import shuffle

def process():
    URL, name = URLInput.get(), NameInput.get()
    text = "".join([i for i in NameInput.get() if i.isalpha()]).lower()

    fname = download_image(URL, name)
    
    encode_message(fname, text, URL)
    
def download_image(URL, name):
    imageCode = get(URL, stream = True)
    
    extension = "." + URL.split(".")[-1].split("/")[0]
    if len(extension) >= 5: extension = ".png"

    fname = os.path.join("x:/VSCode/code", name + extension)

    #check for unsuccessful connection
    if imageCode.status_code != 200: 
        print("failure, path:", fname)
        sleep(2)
        return download_image(URL, name)

    imageCode.raw.decode_content = True

    with open(fname, "wb") as embed:
        shutil.copyfileobj(imageCode.raw, embed)

    return fname

def encode_message(fname, text, URL):
    im = Image.open(fname)
    width, height = im.size

    data = list(im.getdata())
    pixels = im.load()
    
    encoded = [(0,0),(0,1)]
    baseRed = 0
    baseGreen = 0
    baseBlue = 0
    for index, char in enumerate(URL):
        if not index - 1: 
            newPix = (getSudoRandom(stringToNum(fname.split('/')) * width, 0, width), getSudoRandom((stringToNum(fname.split('/')[-1]) + height/2) * height, 0, height))
            if newPix in encoded: 
                newPix[1] += 1
            encoded.append(newPix)
        else:
            seed = ord(char) + index * 2
            while 1:
                newPix = (getSudoRandom(seed * width, 0, width), getSudoRandom((seed + height/2) * height, 0, height))
                if newPix not in encoded: break
                else: seed += newPix[0] * 2
            encoded.append(newPix)
        baseRed += data[encoded[-1][0] + (encoded[-1][1] * width)][0]
        baseGreen += data[encoded[-1][0] + (encoded[-1][1] * width)][1]
        baseBlue += data[encoded[-1][0] + (encoded[-1][1] * width)][2]

    baseRed = int(baseRed / len(encoded))
    baseGreen = int(baseRed / len(encoded))
    baseBlue = int(baseBlue / len(encoded))

    pixels[0,0] = (baseRed, baseGreen, baseBlue)

    URLLen = len(URL)
    URL1 = ceil(URLLen / 3)
    if baseRed > 128: URL1 *= -1
    URLLen -= ceil(URLLen / 3)
    URL2 = ceil(URLLen / 2)
    if baseGreen > 128: URL1 *= -1
    URLLen -= ceil(URLLen / 2)
    if baseBlue > 128: URL1 *= -1
    URL3 = ceil(URLLen)
    print(pixels[0,1])
    print(pixels[0,0])
    pixels[0,1] = (baseRed + URL1, baseGreen + URL2, baseBlue + URL3)
    print(URL1, URL2, URL3)
    print(pixels[0,1])


    for index, point in enumerate(encoded[2:]):
        letterVal = ord(URL[index]) - 74 if ord(URL[index]) >= 64 else 13 # convert a to -13
        Red = ceil(letterVal/3)
        letterVal -= ceil(letterVal/3)
        Green = ceil(letterVal / 2)
        letterVal -= ceil(letterVal / 2)
        Blue = ceil(letterVal)
        pixels[point[0], point[1]] = (int(baseRed + Red), int(baseGreen + Green), int(baseBlue + Blue))

    im.close()

def stringToNum(str : str):
    total = 0
    for i in range(len(str)): total += ord(str[i][0])
    return total

def getSudoRandom(seedNum : int, base : int, top : int):
    seed(seedNum)
    return randint(base, top)

imag = Image.open("X:/Vscode/code/Image.jpg")
print(imag.load()[0,1])

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

#image = open("file.png", "wb")
#image.write(get("https://ichef.bbci.co.uk/news/976/cpsprodpb/E39C/production/_111686285_pic2.png").content)