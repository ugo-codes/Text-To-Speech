from tkinter import Frame, Button, filedialog, messagebox
from gtts import gTTS
import PyPDF2

text = ""
file_name = None


def select_file():
    """
    Tis method opens a file dialog to select a pdf file, returns the file path as string
    :return: (str) the file path to the image file
    """

    global file_name
    # opens a file dialog to select a file
    # sets the title of the file dialog to pick an Image
    file_path = filedialog.askopenfilename(title="Pick A PDF File", filetypes=[("Text Files", ".pdf")])
    if file_path is None:
        return
    # returns the path to the file as string
    file_name = file_path.split("/")[-1]
    file_name = "".join(file_name).split(".")[0]
    return file_path


def open_file():
    """
    This method reads the pdf file and extracts all the text in it
    :return: None
    """
    global text
    pdf_file = select_file()
    # open the file that has been selected by the user
    with open(file=pdf_file, mode="rb") as file:
        # create a filereader object that can perform various tasks
        # from the selected pdf file
        file_reader = PyPDF2.PdfFileReader(file)

        # loop through all the pages in the pdf file then extracts the text in it
        for page_number in range(file_reader.numPages):
            page = file_reader.getPage(page_number)
            text += page.extractText()


def save_audio():
    """
    This method takes the text, converts the text to an audio file then saves it in the directory provided
    :return: None
    """

    global text, file_name
    # if the text is empty or there's no file name don't do anything
    if text == "" or file_name is None:
        return
    # prepares the text to be converted to audio
    audio = gTTS(text=text)
    # get the directory to where to save the audio filr
    directory = filedialog.askdirectory(title="Save Audio")
    # saves the audio file after conversion
    audio.save(f"{directory}/{file_name}.mp3")
    # display a message box to tell the user it's done
    messagebox.showinfo(title="Text To Speech", message="Converted Successfully")

    # sets the text and file_name to the default value
    text = ""
    file_name = None


class StartPage(Frame):

    def __init__(self, parent):
        # initializes the constructor of the super class
        Frame.__init__(self, parent)
        # configure the frame
        # sets the x and y padding, background color
        self.config(padx=10, pady=10)

        # create the button for selecting the pdf file and places it on the screen
        select_file_button = Button(self, text="Select PDF File", command=open_file)
        select_file_button.grid(row=0, column=0)

        # create the button for converting the pdf file to an audio file and places it on the screen
        to_speech_button = Button(self, text="Convert to Audio", command=save_audio)
        to_speech_button.grid(row=0, column=1)
