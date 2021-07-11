from PIL import Image
from requests import get
from io import BytesIO

import requests

def getMessage():
    im = Image.open("X:/Vscode/code/Image.png")
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
    print(savedURL)
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
        unEditColor = unEditPix[newPix[0], newPix[1]]
        Color = pixels[newPix[0], newPix[1]]
        if unEditColor == Color: break
        savedText = savedText + chr(abs(Color[0] - unEditColor[0]) + abs(Color[1] - unEditColor[1]) + 
          abs(Color[2] - unEditColor[2]))
        print(Color, newPix, i)
        i += 1
    del i

    print(savedText)
    for i in savedText: print(ord(i))

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

getMessage()