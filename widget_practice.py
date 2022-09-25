from tkinter import *

root = Tk()

def myClick():
    my_label = Label(root, text="I clicked a button!")
    my_label.pack()


my_button = Button(root, text="Click me!", command=myClick)
my_button.pack()
root.mainloop()