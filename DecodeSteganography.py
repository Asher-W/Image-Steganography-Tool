from random import seed, randint
from PIL import Image
import os

def getMessage():
    im = Image.open("X:/Vscode/code/Image.png")
    width, height = im.size

    pixels = im.load()
    baseColor = pixels[0,0]
    encodedLen = pixels[0,1]

    URLLength = (abs(baseColor[0] - encodedLen[0]) + abs(baseColor[1] - encodedLen[1]) + 
      abs(baseColor[2] - encodedLen[2]))
    encoded = [(0,0),(0,1)]
    savedURL = ""
    for index in range(URLLength):
        if not index: 
            newPix = [getSudoRandom(stringToNum("Image.png") * width, 0, width), 
              getSudoRandom((stringToNum("Image.png") + height/2) * height, 0, height)]
            if newPix in encoded: 
                newPix[1] += 1
            savedURL = savedURL + chr((pixels[newPix[0],newPix[1]][0] - baseColor[0]) + (pixels[newPix[0],newPix[1]][1] - baseColor[1]) + 
              (pixels[newPix[0],newPix[1]][2] - baseColor[2]) + 64)
            encoded.append(newPix)
        else:
            seed = ord(savedURL[-1]) + index * 2
            possibleChange = 1
            while 1:
                newPix = [getSudoRandom(seed * width, 0, width), getSudoRandom((seed + height/2) * height, 0, height)]
                if newPix not in encoded: break
                if newPix[0] < width-possibleChange: newPix[0] +=possibleChange
                if newPix[1] < height-possibleChange: newPix[1] += possibleChange
                if newPix not in encoded: break
                seed += newPix[0] * 2 + possibleChange * 5
                possibleChange += 1
            encoded.append(newPix)
            savedURL = savedURL + chr((pixels[newPix[0],newPix[1]][0] - baseColor[0]) + (pixels[newPix[0],newPix[1]][1] - baseColor[1]) + 
              (pixels[newPix[0],newPix[1]][2] - baseColor[2]) + 64)
    print(savedURL)

def stringToNum(str : str):
    total = 0
    for i in range(len(str)): total += ord(str[i][0])
    return total

def getSudoRandom(seed, base, top):
    seed, base, top = int(seed), int(base), int(top)
    seedBin = bin(seed)[2:]
    endbin = bin(top)[2:]
    extraZeros = len(seedBin) - len(endbin)
    if extraZeros > 0:
        for i in range(0, extraZeros, 1): endbin = "0" + endbin
    if extraZeros < 0:
        for i in range(0, extraZeros, -1): seedBin = "0" + seedBin
    returnNum = ""
    for i in range(len(returnNum)):
        if returnNum[i] == endbin[i]: returnNum = returnNum + "0"
        else: returnNum = returnNum + "1"
    num = 0
    for i, v in enumerate(returnNum):
        num += i ** v
    returnNum = num
    del num
    return min(max((returnNum ** 3 + base) ** 2 % (top - base), base), top - 1)

getMessage()