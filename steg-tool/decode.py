import tkinter as tk
from tkinter import filedialog
from PIL import Image
from requests import get
from io import BytesIO

def getMessage(file_name):
    # make sure the file is selected
    if ".png" not in file_name: return
    # open the slelected file and get base info 
    im = Image.open(file_name)
    width, height = im.size
    pixels = im.load()

    base_color = pixels[0,0] # get the reference color for decoding the URL

    encoded_len = pixels[0,1] # get the pixel values storing the stored URL's length
    URL_length = (abs(base_color[0] - encoded_len[0]) + abs(base_color[1] - encoded_len[1]) + 
      abs(base_color[2] - encoded_len[2]))  # decode the encoded URL pixel

    encoded_pix = [[0,0],[0,1]] # list to store in-use pixels

    saved_URL = ""
    for index in range(URL_length):
        if not index: seed = string_to_num(file_name.split('/')[-1]) + 1 # assigns the seed for the first character
        else: seed = ord(saved_URL[-1]) + index * 2 # uses the ascii value of the previous character and the index to assign the seed

        pos_change = 1 # use a incrementing value, so seed canges can't get stuck in a loop
        # get the new pixel to read from and verify that it isn't already in use
        while 1:
            new_pix = [get_sudo_random(seed * width, 0, width), get_sudo_random((seed + height/2) * height, 0, height)]
            if new_pix not in encoded_pix: break
            seed = get_sudo_random(seed, 0, width) + pos_change
            pos_change += 1

        encoded_pix.append(new_pix)

        # get and decode the next pixel
        pixel_color = pixels[new_pix[0],new_pix[1]]
        saved_URL = saved_URL + chr(abs(base_color[0] - pixel_color[0]) + abs(base_color[1] - pixel_color[1]) + 
          abs(base_color[2] - pixel_color[2]))

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
            new_pix = [get_sudo_random(seed * width, 0, width), get_sudo_random((seed + height/2) * height, 0, height)]
            if new_pix not in encoded_pix: break 
            seed = get_sudo_random(seed, 0, width) + pos_change
            pos_change += 1
        
        encoded_pix.append(new_pix)

        #find the original and changed color, then decode it
        unedited_color = unedited_pix[new_pix[0], new_pix[1]]
        color = pixels[new_pix[0], new_pix[1]]
        if unedited_color == color: break # check if the pixels are the same
        saved_text = saved_text + chr(abs(color[0] - unedited_color[0]) + abs(color[1] - unedited_color[1]) + 
          abs(color[2] - unedited_color[2]))

        index += 1 #increment the index value for the next loop

    TextOutput["text"] = saved_text # update the tkinter window to display found text

#convert a supplied string to a usable integer
def string_to_num(str : str):
    total = 0
    for i in range(len(str)): total += ord(str[i][0])
    return total

#take in a seed base and top to give a semi-random number
def get_sudo_random(seed, base, top):
    seed, base, top = int(seed), int(base), int(top) # make sure inputs are the proper format
    
    #remove the 0b string from the beggining of the binary string
    seed_binary = bin(seed)[2:]
    top_binary = bin(top)[2:]

    #make sure both strings are the same length, and add to the begging of the shorter one
    extra_zeros = len(seed_binary) - len(top_binary)
    if extra_zeros > 0:
        for i in range(0, extra_zeros, 1): top_binary = "0" + top_binary
    if extra_zeros < 0:
        for i in range(0, extra_zeros, -1): seed_binary = "0" + seed_binary
    
    #preform and XOR (exclusive or) function on the top and seed binary
    return_num = ""
    for index in range(len(top_binary)):
        if seed_binary[i] == top_binary[index]: return_num = return_num + "0"
        else: return_num = return_num + "1"
    
    #convert the number back to integer
    num = 0
    for index, value in enumerate(return_num):
        num += int(value) * 2 ** index
    return_num = num
    del num

    return min(max(((return_num ** 3 + base) ** 2 % (top - base)) + base, base), top - 1) #further randomize the returned number

#run the getMessage function and ask for the png file
def select_file():
    getMessage(filedialog.askopenfilename(initialdir= "/", filetypes=(("png files", "png {*.png}"))))

# don't execute if the file is imported
if __name__ == "__main__":
    # create the object to hold widgets
    root = tk.Tk()
    # edit geometry of the window
    root.geometry("500x500")
    root.resizable(0,0)

    # whole storage area
    main_frame = tk.Frame(root)

    # find the image
    file_label = tk.Label(main_frame, text = "select your file", font = "Verdana 15").pack()
    file_select = tk.Button(main_frame, command = select_file, text = "file").pack(pady = 10)

    # take text details
    TextLabel = tk.Label(main_frame, text="Encoded text", font = "Verdana 15").pack(pady = 20)
    TextOutput = tk.Label(main_frame, text = "no file selected").pack()

    # show widgets (using pack)
    main_frame.pack(expand=1,fill=tk.BOTH, padx = 10, pady = 10)

    # show the window and widgets
    root.mainloop()