from tkinter import *

class Application:
	def __init__(self, master=None):
		master.title("Projeto IA")
		self.widget1 = Frame(master)
		self.widget1.pack()
		self.msg = Label(self.widget1, text="Favor selecione a Base de dados a ser utilizada")
		self.msg["font"] = ("Calibri", "10", "bold")
		self.msg.pack ()
		self.button1 = Button(self.widget1)
		self.button1["text"] = "cifar10"
		self.button1["font"] = ("Calibri", "9")
		self.button1["width"] = 10
		self.button1.bind("<Button-1>", self.selBut1)
		self.button1["command"] = self.widget1.quit
		self.button1.pack ()
		self.button2 = Button(self.widget1)
		self.button2["text"] = "mnist"
		self.button2["font"] = ("Calibri", "9")
		self.button2["width"] = 10
		self.button2.bind("<Button-1>", self.selBut2)
		self.button2["command"] = self.widget1.quit
		self.button2.pack ()

	def selBut1(self, event):
		self.dataset = "cifar10"

	def selBut2(self, event):
		self.dataset = "mnist"

