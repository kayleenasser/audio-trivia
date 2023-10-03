from tkinter import *
import constants as constants


root = Tk()
root.title(constants.APP_TITLE)

lbl_hello = Label(root, text="Hello, world!")
lbl_hello.pack()



root.mainloop()