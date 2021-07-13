import tkinter as tk
from tkinter import filedialog
import decoder
import encoder

def open_encoder():
    # create the object to hold widgets
    root = tk.Toplevel()
    # edit geometry of the window
    root.geometry("500x500")
    root.resizable(0,0)
    
    # name the window
    root.title("Encoder")

    # whole storage area
    main_frame = tk.Frame(root)

    # take image details
    URL_label = tk.Label(main_frame, text="Image URL")
    URL_input = tk.Text(main_frame, width = 50, height = 2)

    # take image details
    name_label = tk.Label(main_frame, text="Image file Name (always a png)")
    name_input = tk.Text(main_frame, width = 50, height = 1)

    # find where to store the image
    global folder 
    folder = "/"
    folder_select = tk.Button(main_frame, command = select_folder, text = "select folder")

    # take text details
    text_label = tk.Label(main_frame, text="Encoded")
    text_input = tk.Text(main_frame, width = 75, height = 10)

    # show widgets (using pack)
    main_frame.pack(expand=1,fill=tk.BOTH, padx = 10, pady = 10)

    URL_label.pack()
    URL_input.pack()
    name_label.pack()
    name_input.pack()

    folder_select.pack(pady = 10)

    text_label.pack()
    text_input.pack()

    # submit button
    submit = tk.Button(main_frame, command = lambda: encoder.process(URL_input.get("1.0","end"), 
      text_input.get("1.0","end"), name_input.get("1.0", "end"), folder), text = "process").pack()

# ask for a folder to write to
def select_folder():
    global folder
    if folder: folder = filedialog.askdirectory(initialdir="")

def open_decoder():
    # create the object to hold widgets
    root = tk.Toplevel()
    # edit geometry of the window
    root.geometry("500x500")
    root.resizable(0,0)
    
    # name the window
    root.title("Decoder")

    # whole storage area
    main_frame = tk.Frame(root)

    # find the image
    tk.Label(main_frame, text = "select your file", font = "Verdana 15").pack()
    tk.Button(main_frame, command = select_file, text = "file").pack(pady = 10)

    # take text details
    tk.Label(main_frame, text="Encoded text", font = "Verdana 15").pack(pady = 20)
    global text_output
    text_output = tk.Label(main_frame, text = "no file selected")
    text_output.pack()

    # show widgets (using pack)
    main_frame.pack(expand=1,fill=tk.BOTH, padx = 10, pady = 10)

#run the getMessage function and ask for the png file
def select_file():
    file = filedialog.askopenfilename(initialdir= "/", filetypes=(("png files", "png {*.png}")))
    if file: 
        global text_output
        text_output["text"] = decoder.getMessage(file)

# only run if this is the root folder
if __name__ == "__main__":
    # create the parent window to open the encoder/decoder
    root = tk.Tk()
    # edit the size of root
    root.geometry("400x150")
    root.resizable(0,0)
    
    # name the window
    root.title("Image Steganography")

    # make xontainers
    title_frame = tk.Frame(root)
    main_frame = tk.Frame(root)

    #write the title
    tk.Label(root, text = "Image Steganography", font = "Veranda 15").pack()
    tk.Label(root, text = "By Asher-W", font = "Veranda 12").pack()
    tk.Label(root, text = "Asisted by J-nac", font = "Veranda 12").pack()

    # create the buttons to open the encoder and decoder
    encode = tk.Button(main_frame, command = open_encoder, width = 15, text = "Open Encoder", font = "Verdana 15")
    decode = tk.Button(main_frame, command = open_decoder, width = 15, text = "Open Decoder", font = "Verdana 15")

    # display the container and widgets
    title_frame.pack(expand = 1, fill = tk.BOTH)
    main_frame.pack(padx = 5, pady = 3, fill = tk.BOTH, expand = 1)
    encode.pack(side = tk.LEFT)
    decode.pack(side = tk.RIGHT)

    # open and handle the window
    root.mainloop()