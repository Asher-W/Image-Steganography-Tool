from random import seed, randint
from PIL import Image

def getMessage():
    im = Image.open("X:/Vscode/code/Image.jpg")
    width, height = im.size

    data = list(im.getdata())
    baseColor = data[0]

    URLLength = (abs(baseColor[0] - data[1][0]) + abs(baseColor[1] - data[1][1]) + 
      abs(baseColor[2] - data[1][2]))
    print(URLLength, data[1])

def stringToNum(str : str):
    total = 0
    for i in range(len(str)): total += ord(str[i][0])
    return total

def getSudoRandom(seedNum : int, base : int, top : int):
    seed(seedNum)
    randint(base, top)

getMessage()