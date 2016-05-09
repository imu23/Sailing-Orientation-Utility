from Tkinter import *#Tk, RIGHT, LEFT, BOTH, RAISED
from ttk import Frame, Button, Style


class testGui(Frame):
  
	def __init__(self, parent):
		Frame.__init__(self, parent)   
		 
		self.parent = parent
		self.initUI()

		
	def initUI(self):
	  	self.parent.title("Sailing Orientation")
		self.style = Style()
		self.style.theme_use("default")
		
		
		#Frames
		tempFrame = Frame(self, relief=RAISED, borderwidth=1)
		tempFrame.pack(fill=BOTH, expand=True)
		
		altFrame = Frame(self, relief=RAISED, borderwidth=1)
		altFrame.pack(fill=BOTH, expand=True)
		
		posFrame = Frame(self, relief=RAISED, borderwidth=1)
		posFrame.pack(fill=BOTH, expand=True)
		
		accFrame = Frame(self, relief=RAISED, borderwidth=1)
		accFrame.pack(fill=BOTH, expand=True)
		
		pressFrame = Frame(self, relief=RAISED, borderwidth=1)
		pressFrame.pack(fill=BOTH, expand=True)
		
		headFrame = Frame(self, relief=RAISED, borderwidth=1)
		headFrame.pack(fill=BOTH, expand=True)
		
		timeFrame = Frame(self, relief=RAISED, borderwidth=1)
		timeFrame.pack(fill=BOTH, expand=True)
		
		self.pack(fill=BOTH, expand=True)
		
		
		#Buttons
		saveButton = Button(self, text="Save")
		saveButton.pack(anchor=S, side=RIGHT, padx=5, pady=5)
		playButton = Button(self, text="Play/Pause")
		playButton.pack(anchor=S, side=LEFT, padx=5, pady=5)
		
		#StringVars
		self.tempStr = StringVar()
		self.altStr = StringVar()
		self.posStr = StringVar()
		self.accStr = StringVar()
		self.pressStr = StringVar()
		self.headStr = StringVar()
		self.timeStr = StringVar()

		#Labels
		tempLabel = Label(tempFrame, text="Temperature:")
		tempLabel.pack(expand=True, side=LEFT)
		temp = Label(tempFrame, textvariable=self.tempStr)
		temp.pack(expand=True, side=LEFT)
		
		altLabel = Label(altFrame, text="alt:")
		altLabel.pack(expand=True, side=LEFT)
		alt = Label(altFrame, textvariable=self.altStr)
		alt.pack(expand=True, side=LEFT)
		
		posLabel = Label(posFrame, text="pos:")
		posLabel.pack(expand=True, side=LEFT)
		pos = Label(posFrame, textvariable=self.posStr)
		pos.pack(expand=True, side=LEFT)
		
		accLabel = Label(accFrame, text="accel:")
		accLabel.pack(expand=True, side=LEFT)
		acc = Label(accFrame, textvariable=self.accStr)
		acc.pack(expand=True, side=LEFT)
		
		pressLabel = Label(pressFrame, text="press:")
		pressLabel.pack(expand=True, side=LEFT)
		press = Label(pressFrame, textvariable=self.pressStr)
		press.pack(expand=True, side=LEFT)
		
		headLabel = Label(headFrame, text="head:")
		headLabel.pack(expand=True, side=LEFT)
		head = Label(headFrame, textvariable=self.headStr)
		head.pack(expand=True, side=LEFT)
		
		timeLabel = Label(timeFrame, text="time:")
		timeLabel.pack(expand=True, side=LEFT)
		time = Label(timeFrame, textvariable=self.timeStr)
		time.pack(expand=True, side=LEFT)
		
		self.tempStr.set("Null")
		self.altStr.set("Null")
		self.posStr.set("Null")
		self.accStr.set("Null")
		self.pressStr.set("Null")
		self.headStr.set("Null")
		self.timeStr.set("Null")

	#Utility Setter Methods    
	def setTemp(self, temp):
		self.tempStr.set(temp)
		
	def setAccel(self, accel):
		self.accStr.set(accel)
        #self.after(200, setAccel)
		
	def setHeading(self, head):
		self.headStr.set(head)
		
	def setPress(self, press):
		self.pressStr.set(press)

	def setPos(self, lat, lon):
		self.posStr.set(lat + ", " + lon)
		
	def setAlt(self, alt):
		self.altStr.set(alt)
				
	def setTime(self, time, date):
		self.timeStr.set(date + " " + time)
              

def main():
  
    root = Tk()
    root.geometry("300x200+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main() 
