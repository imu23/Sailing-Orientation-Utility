from guiTest import *
from Tkinter import *
from ttk import Frame, Button, Style

def main():
    root = Tk()
    gui = testGui(root)
    root.geometry("300x200+300+300")
    
    root.after(200, gui.setAccel("hi"))
    #root.mainloop()
    root.Update()
    root.after(200, gui.setHeading("POOP"))

if __name__ == '__main__':
    main()
