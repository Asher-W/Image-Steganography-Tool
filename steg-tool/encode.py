import tkinter as tk
from PIL import Image
from requests import get
from io import BytesIO

# get the input values and pass it onto the encode function
def process(URL_input, text_input, name_input):
    URL, text, name = URL_input.get(), text_input.get(), name_input.get()
    
    encode_message(name, text, URL)

# encode the text variable in the image
def encode_message(name, text, URL):
    # get the image info from the url
    request = get(URL)
    if request.status_code != 200:
        print("Connection Issue, error code: {}".format(request.status_code))
        return
    
    im = Image.open(BytesIO(request.content)) # use BytesIO to convert the request to usable image code
    file_name = folder + "/" + name + ".png" # make a path variable to the file

    width, height = im.size # get image information

    pixels = im.load() # im pixel data

    # apply max text length
    if len(text) > (width * height - 2) / 2: text = text[:(width * height - 2) / 2]
    
    # store pixels that are in-use
    encoded_pix = [[0,0],[0,1]]

    # variables to find average color for encoding the URL
    base_red = 0
    base_green = 0
    base_blue = 0

    # loop through the URL and find where to puth the encoded pixels
    for index in range(len(URL)):
        if not index: seed = string_to_num(file_name.split('/')[-1]) + 1 # get a seed based on the file name
        else: seed = ord(URL[index - 1]) + index * 2 # get a seed based on the previous character's ascii value and index

        pos_change = 1 # use a incrementing value, so seed canges can't get stuck in a loop
        # get the new pixel to read from and verify that it isn't already in use
        while 1:
            new_pix = [get_sudo_random(seed * width, 0, width), get_sudo_random((seed + height/2) * height, 0, height)]
            if new_pix not in encoded_pix: break
            seed = get_sudo_random(seed, 0, width) + pos_change
            pos_change += 1
        
        encoded_pix.append(new_pix)

        # base colors incremented for calculating averages
        base_red += pixels[encoded_pix[-1][0], encoded_pix[-1][1]][0]
        base_green += pixels[encoded_pix[-1][0], encoded_pix[-1][1]][1]
        base_blue += pixels[encoded_pix[-1][0], encoded_pix[-1][1]][2]

    # calculating the average value for base colors
    base_red = int(base_red / len(encoded_pix))
    base_green = int(base_red / len(encoded_pix))
    base_blue =  int(base_blue / len(encoded_pix))

    pixels[0,0] = (base_red, base_green, base_blue) # store the average values in the image

    # split the URL length through RGB
    URL_len = len(URL)

    URL1 = int(URL_len / 3)
    if base_red > 128: URL1 *= -1
    URL_len -= int(URL_len / 3)

    URL2 = int(URL_len / 2)
    if base_green > 128: URL2 *= -1
    URL_len -= int(URL_len / 2)

    URL3 = int(URL_len)
    if base_blue > 128: URL3 *= -1

    # apply the distributed length too the second pixel
    pixels[0,1] = (base_red + URL1, base_green + URL2, base_blue + URL3)

    # loop through the found pixels to be encoded and 
    for index, point in enumerate(encoded_pix[2:]):
        # find the ascii value for the character being encoded
        letter_val = ord(URL[index])

        # distribute the number over RGB values
        red = int(letter_val/3)
        if base_red > 128: red *= -1
        letter_val -= int(letter_val/3)

        green = int(letter_val / 2)
        if base_green > 128: green *= -1
        letter_val -= int(letter_val / 2)

        blue = int(letter_val)
        if base_blue > 128: blue *= -1

        # apply the RGB values
        pixels[point[0], point[1]] = (base_red + red, base_green + green, base_blue + blue)
    
    for index, value in enumerate(text):
        if not index: seed = ord(URL[-1]) + 1 # get a seed based on the last char of the URL
        else: seed = ord(text[index - 1]) + index * 2 # get a seed based on the previous character in the text and the index
        
        pos_change = 1 # use a incrementing value, so seed canges can't get stuck in a loop
        # get the new pixel to write to and verify that it isn't already in use
        while 1:
            new_pix = [get_sudo_random(seed * width, 0, width), get_sudo_random((seed + height/2) * height, 0, height)]
            if new_pix not in encoded_pix: break
            seed = get_sudo_random(seed, 0, width) + pos_change
            pos_change += 1

        encoded_pix.append(new_pix)

        letter_val = max(ord(value), 1) # get the ascii value of the letter being encoded
        
        colors = pixels[new_pix[0], new_pix[1]] # get the unedited colors

        # distribute the value between RGB values
        red = int(letter_val/3)
        if colors[0] > 128: red *= -1
        letter_val -= int(letter_val/3)

        green = int(letter_val / 2)
        if colors[1] > 128: green *= -1
        letter_val -= int(letter_val / 2)

        blue = int(letter_val)
        if colors[2] > 128: blue *= -1

        # apply the adjusted RGB values relative to the unedited pixel
        pixels[new_pix[0], new_pix[1]] = (colors[0] + red, colors[1] + green, colors[2] + blue)

    im.save(file_name) # save the image code to the png file
    im.close() # close the file reference

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

# ask for a folder to write to
def select_folder():
    folder = tk.filedialog.askdirectory(initialdir="")
    print(folder)

# don't execute if the file is imported
if __name__ == "__main__":
    # create the object to hold widgets
    root = tk.Tk()
    # edit geometry of the window
    root.geometry("500x500")
    root.resizable(0,0)

    # whole storage area
    main_frame = tk.Frame(root)

    # take image details
    URL_label = tk.Label(main_frame, text="Image URL")
    URL_input = tk.Text(main_frame, width = 50, height = 2)

    # take image details
    name_label = tk.Label(main_frame, text="Image file Name (always a png)")
    name_input = tk.Entry(main_frame)

    # find where to store the image
    folder = "/"
    folder_select = tk.Button(main_frame, command = select_folder, text = "folder")

    # take text details
    text_label = tk.Label(main_frame, text="Encoded text")
    text_input = tk.Text(main_frame, width = 75, height = 10)

    # show widgets (using pack)
    main_frame.pack(expand=1,fill=tk.BOTH, padx = 10, pady = 10)

    URL_label.pack()
    URL_input.pack()
    name_label.pack()
    name_input.pack()
    folder_select.pack()

    text_label.pack()
    text_input.pack()

    # submit button
    tk.Button(main_frame, command = lambda: process(URL_input, name_input, text_input), text = "process").pack()

    # show the window and widgets
    root.mainloop()