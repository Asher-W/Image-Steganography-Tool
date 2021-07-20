from PIL import Image
from requests import get
import shared_functions as sf
from math import sqrt
from io import BytesIO

# get the input values and pass it onto the encode function
def process(URL, text, name, folder):
    # verify a valid file name
    name = "".join(char for char in name if char in "()_-,. " or char.isalpha() or char.isnumeric())
    if len(name) > 100: name = name[:100]

    # make sure the folder var is a valid path and that the file is named
    if ":" not in folder or not len(name): return

    name = folder + "/" + name + ".png" # make a path variable to the file
    
    encode_message(name, text, URL)

# encode the text variable in the image
def encode_message(file_name, text, URL):
    # get the image info from the url
    request = get(URL.strip())
    if request.status_code != 200:
        print("Connection Issue, error code: {}".format(request.status_code))
        return
    
    im = Image.open(BytesIO(request.content)) # use BytesIO to convert the request to usable image code

    width, height = im.size # get image information

    pixels = im.load() # im pixel data

    # apply max text length
    if len(text) > (width * height - 2) / 2: text = text[:(width * height - 2) / 2]
    
    # store pixels that are in-use
    encoded_pix = [(0,0),(0,1)]

    # variables to find average color for encoding the URL
    base_red, base_green, base_blue = 0, 0, 0

    #remove newlines and excess spaces from the ends of the URL
    URL = URL.strip()

    # loop through the URL and find where to puth the encoded pixels
    for index in range(len(URL)):
        if not index: seed = sf.string_to_num(file_name.split('/')[-1]) + 1 # get a seed based on the file name
        else: seed = ord(URL[index - 1]) + index * 2 # get a seed based on the previous character's ascii value and index
        pos_change = 1 # use a incrementing value, so seed changes can't get stuck in a loop

        # get the new pixel to read from and verify that it isn't already in use
        while 1:
            new_pix = (sf.get_sudo_random(seed * width, 0, width), sf.get_sudo_random((seed ** 2) * height, 0, height))
            if new_pix not in encoded_pix: break
            seed = sf.get_sudo_random(seed + pos_change, 0, width)
            pos_change += 1

        # base colors incremented for calculating averages
        base_red += pixels[new_pix[0], new_pix[1]][0]
        base_green += pixels[new_pix[0], new_pix[1]][1]
        base_blue += pixels[new_pix[0], new_pix[1]][2]

        encoded_pix.append(new_pix)


    # calculating the average value for base colors
    base_red = int(base_red / len(encoded_pix))
    base_green = int(base_green / len(encoded_pix))
    base_blue =  int(base_blue / len(encoded_pix))

    pixels[0,0] = (base_red, base_green, base_blue) # store the average values in the image

    # split the URL length through RGB
    URL_len = len(URL)

    URL1, URL_2_3 = get_root_and_rem(URL_len)

    URL2, URL3 = int(URL_2_3 / 2), URL_2_3 - int(URL_2_3 / 2)

    if base_red > 128: URL1 *= -1
    if base_green > 128: URL2 *= -1
    if base_blue > 128: URL3 *= -1

    # apply the distributed length too the second pixel
    pixels[0,1] = (base_red + URL1, base_green + URL2, base_blue + URL3)

    # loop through the found pixels to be encoded and encode the value
    for index in range(len(encoded_pix) - 2):
        #check to end the loop
        if index >= len(encoded_pix): break

        # find the ascii value for the character being encoded
        letter_val = ord(URL[index])

        red, green_blue = get_root_and_rem(letter_val)

        green, blue = int(green_blue / 2), green_blue - int(green_blue / 2) 

        if base_red > 128: red *= -1
        if base_green > 128: green *= -1
        if base_blue > 128: blue *= -1

        # apply the RGB values
        point = encoded_pix[index + 2]
        pixels[point[0], point[1]] = (base_red + red, base_green + green, base_blue + blue)
    
    for index, value in enumerate(text):
        if not index: seed = ord(URL[-1]) + 1 # get a seed based on the last char of the URL
        else: seed = ord(text[index - 1]) + index * 2 # get a seed based on the previous character in the text and the index
        
        pos_change = 1 # use a incrementing value, so seed canges can't get stuck in a loop
        # get the new pixel to write to and verify that it isn't already in use
        while 1:
            new_pix = (sf.get_sudo_random(seed * width, 0, width), 
              sf.get_sudo_random((seed + height/2) * height, 0, height))
            if new_pix not in encoded_pix: break
            seed = sf.get_sudo_random(seed + pos_change, 0, width)
            pos_change += 1

        encoded_pix.append(new_pix)

        letter_val = min(max(ord(value), 1), 255) # get the ascii value of the letter being encoded
        
        colors = pixels[new_pix[0], new_pix[1]] # get the unedited colors

        red, green_blue = get_root_and_rem(letter_val)

        green, blue = int(green_blue / 2), green_blue - int(green_blue / 2) 

        if base_red > 128: red *= -1
        if base_green > 128: green *= -1
        if base_blue > 128: blue *= -1

        # apply the adjusted RGB values relative to the unedited pixel
        pixels[new_pix[0], new_pix[1]] = (colors[0] + red, colors[1] + green, colors[2] + blue)
        
    im.save(file_name) # save the image code to the png file
    im.close() # close the file reference

def get_root_and_rem(num):
    square = int(sqrt(num))
    rem = num - (square ** 2)

    return (square, rem)