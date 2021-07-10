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
        else:
            seed = ord(savedURL[-1]) + index * 2
            while 1:
                newPix = [getSudoRandom(seed * width, 0, width), getSudoRandom((seed + height/2) * height, 0, height)]
                if newPix not in encoded: break
                seed += newPix[0] * 2 + 1
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

    return min(max((returnNum ** 3 + base) ** 2 % (top - base), base), top - 1)

getMessage()