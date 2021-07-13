import tkinter as tk
import decoder
import encoder

def open_encoder():
    # create the object to hold widgets
    root = tk.Toplevel()
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
    tk.Button(main_frame, command = lambda: encoder.process(URL_input, name_input, text_input), text = "process").pack()

# ask for a folder to write to
def select_folder():
    folder = tk.filedialog.askdirectory(initialdir="")

def open_decoder():
    # create the object to hold widgets
    root = tk.Toplevel()
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

#run the getMessage function and ask for the png file
def select_file():
    decoder.getMessage(tk.filedialog.askopenfilename(initialdir= "/", filetypes=(("png files", "png {*.png}"))))

# only run if this is the root folder
if __name__ == "__main__":
    # create the parent window to open the encoder/decoder
    root = tk.Tk()
    # edit the size of root
    root.geometry("300x75")
    root.resizable(0,0)

    # make a container to hold the buttons
    main_frame = tk.Frame(root)

    # create the buttons to open the encoder and decoder
    encode = tk.Button(main_frame, command = open_encoder, width = 9, text = "encoder", font = "Verdana 15")
    decode = tk.Button(main_frame, command = open_decoder, width = 9, text = "decoder", font = "Verdana 15")

    # display the container and widgets
    main_frame.pack(padx = 5, pady = 3, fill = tk.BOTH, expand = 1)
    encode.pack(side = tk.LEFT)
    decode.pack(side = tk.RIGHT)

    # open and handle the window
    root.mainloop()