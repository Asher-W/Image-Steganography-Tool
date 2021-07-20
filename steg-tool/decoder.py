from PIL import Image
import shared_functions as sf
from requests import get
from io import BytesIO

from math import sqrt

def getMessage(file_name):
    # make sure the file is selected
    if ".png" not in file_name: return
    # open the slelected file and get base info 
    im = Image.open(file_name)
    width, height = im.size
    pixels = im.load()

    base_color = pixels[0,0] # get the reference color for decoding the URL

    encoded_len = pixels[0,1] # get the pixel values storing the stored URL's length
    
    URL_length = ((abs(base_color[0] - encoded_len[0]) ** 2) + abs(base_color[1] - encoded_len[1]) + abs(base_color[2] - encoded_len[2]))  # decode the encoded URL pixel

    encoded_pix = [(0,0),(0,1)] # list to store in-use pixels

    saved_URL = ""
    for index in range(URL_length):
        if not index: seed = sf.string_to_num(file_name.split('/')[-1]) + 1 # assigns the seed for the first character
        else: seed = ord(saved_URL[-1]) + index * 2 # uses the ascii value of the previous character and the index to assign the seed

        pos_change = 1 # use a incrementing value, so seed canges can't get stuck in a loop
        # get the new pixel to read from and verify that it isn't already in use
        while 1:
            new_pix = (sf.get_sudo_random(seed * width, 0, width), 
              sf.get_sudo_random((seed ** 2) * height, 0, height))
            if new_pix not in encoded_pix: break
            seed = sf.get_sudo_random(seed + pos_change, 0, width)
            pos_change += 1

        encoded_pix.append(new_pix)

        # get and decode the next pixel
        pixel_color = pixels[new_pix[0],new_pix[1]]
        # check or impropper inputs
        try:
            saved_URL = saved_URL + chr((abs(base_color[0] - pixel_color[0]) ** 2) + abs(base_color[2] - pixel_color[2]) + abs(base_color[1] - pixel_color[1]))
        except ValueError: 
            return "Improper file"

    # get the unedited image from the url, and check for a proper connection
    request = get(saved_URL)
    if request.status_code != 200:
        print("Connection Issue, error code: {}".format(request.status_code))
        return
    unedited = Image.open(BytesIO(request.content)) # use bytesIO to convert the request content to readable data for pillow (PIL)
    unedited_pix = unedited.load()

    # iterate throught the image untill there isn't a difference between both found pixels
    index = 0
    saved_text = ""
    while 1:
        if not index: seed = ord(saved_URL[-1]) + 1 # set the seed based on the last character in the URL
        else: seed = ord(saved_text[index - 1]) + index * 2 # set the seed based on the previous charcter and index
        pos_change = 1

        # find the next pixel and verify that they aren't already in use
        while 1:
            new_pix = (sf.get_sudo_random(seed * width, 0, width), 
              sf.get_sudo_random((seed + height/2) * height, 0, height))
            if new_pix not in encoded_pix: break 
            seed = sf.get_sudo_random(seed + pos_change, 0, width)
            pos_change += 1
        
        encoded_pix.append(new_pix)

        #find the original and changed color, then decode it
        unedited_color = unedited_pix[new_pix[0], new_pix[1]]
        color = pixels[new_pix[0], new_pix[1]]
        if unedited_color == color: break # check if the pixels are the same
        saved_text = saved_text + chr((abs(color[0] - unedited_color[0]) ** 2) + abs(color[1] - unedited_color[1]) + abs(color[2] - unedited_color[2]))

        index += 1 #increment the index value for the next loop
    if saved_text:    
        return saved_text # update the tkinter window to display found text
    else: return "Improper file"