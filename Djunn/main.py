#计算器
import math
from math import cos,sin,sqrt,log
import tkinter as tk
import tkinter.messagebox

from compute import myEvalTemp

VERSION = 1.4
BUTTONS = [['C', '/', '*', '<-'],
           ['7', '8', '9', '-'],
           ['4', '5', '6', '+'],
           ['1', '2', '3', '.'],
           ['(', '0', ')', '='],
           ['cos','sin','ln','sqrt'],
           ['^','E','Pi','!']]  # Give them to .grid()
           # ^ 表示乘方， ！表示阶乘

class Calculator(tk.Frame):
    def __init__(self,master = None, rows = 7):
        super().__init__(master)
        self.rows = rows #表示有(几行+1)按钮
        self.perRow = 4 #表示一行有多少个按钮
        self.master = master
        self.createMenu()
        self.var = tk.StringVar() 
        mainWindow = tk.Label(master, bg='white',fg='black', textvariable=self.var, 
        anchor="nw", justify="left",wraplength = 290,font=('Arial',12), width=30,height=3)
        mainWindow.grid(row=0,column=0,ipadx=20,ipady=20,columnspan=4)
        for i in range(self.rows):
            for j in range(self.perRow):
                symbol = BUTTONS[i][j]
                if symbol=='C':
                    f = self.clear
                elif symbol=='=':
                    f = self.equal
                elif symbol=='<-':
                    f = self.backspace
                else:
                    f = lambda s=symbol:self.var.set(self.var.get()+s)
 
                tk.Button(root,command = f, text=symbol, width=3,height=1).grid(
                    row=i+1,column=j,ipadx=10,ipady=10,padx=6,pady=6,sticky='w')

    def createMenu(self):
        menuBar = tk.Menu(self.master)
        settingMenu = tk.Menu(menuBar, tearoff=0)
        aboutMenu = tk.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Settings", menu = settingMenu)
        menuBar.add_cascade(label="About",menu = aboutMenu)
        aboutMenu.add_command(label="Version "+str(VERSION))
        #settingMenu.add_checkbutton(label="Extension(Exp)",command=self.extension)
        self.master.config(menu = menuBar)

    def extension(self):
        self.__init__(self.master, 6)

    def clear(self):
        self.var.set('')

    def equal(self):
        if self.var.get()=="Error":
            self.var.set('')  
        try:
            #exp=re.sub(r'ln|E|Pi|\-?\d+(.\d+)?\!|\^',replace,self.var.get())
            exp = self.var.get()
            if not exp:
                raise ValueError
            res = myEvalTemp(exp)
            self.var.set(str(res))
        except SyntaxError:
            self.var.set("Error")
        except BaseException:
            pass

    def backspace(self):
        self.var.set(self.var.get()[:-1])

if __name__ == '__main__':
    root = tk.Tk()
    app = Calculator(root)
    app.master.title("Calculator")
    app.master.geometry("300x450")
    app.master.minsize(height=540, width=300)
    app.master.maxsize(height=540, width=300)
    app.mainloop()