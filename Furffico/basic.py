import time
from sys import exit, argv
from PyQt5.Qt import QCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel

BASE = 30  # X button size(px)

def nFormat(n):
    return f'{n:.3f}' if isinstance(n,float) else str(n)

def logger(event: str, pre=""):
    print(pre+time.strftime("[%Y-%m-%d %H:%M:%S] ",time.localtime())+event.replace('\n', '\\n'))

class MainWindow(QMainWindow):

    def __init__(self,calculator,title):
        logger("Initializing.")
        super().__init__()
        self.calculator=calculator
        self.windowtitle=title
        self.UIinit()
        logger("Initialized.")

    def UIinit(self):
        self.btn = {}
        self.m_flag = False
        BASE2 = BASE*2
        #! window ===========================================
        W, H = BASE2*max(map(len,self.calculator.keyboard)), BASE2*(2+len(self.calculator.keyboard))
        self.setFixedSize(W,H)
        self.setWindowFlag(2048) # Qt.FramelessWindowHint=2048
        self.setAttribute(120, True) # Qt.WA_TranslucentBackground=120
        # 好像样式表不能和程序一起打包呢、、、只好写进程序了
        self.setStyleSheet("*{color:#000;font-family:Consolas;border:0;padding:5px 2px 5px 2px;background:rgba(200,200,200,.8)}QLabel#title{font-size:15px}QLabel#subscreen{font-size:20px;padding-right:5px}QLabel#screen{font-size:25px}QPushButton.keyboard{font-size:24px}QPushButton.keyboard:hover{background:#c8c8c8}QPushButton#close{background:rgba(255,170,170,.8);font-size:15px}QPushButton#close:hover{background:#faa}")

        #! labels ===========================================
        def genLabel(window, id, rect, caption, pclass=None):
            lb = QLabel(window)
            lb.setGeometry(*rect)
            lb.setText(caption)
            lb.setObjectName(id)
            if pclass:
                lb.setProperty('class', pclass)
            return lb

        self.title = genLabel(self, "title", (0, 0, W-BASE, BASE), self.windowtitle)
        self.subscreen = genLabel(self, "subscreen", (0, BASE, W, BASE), "")
        self.subscreen.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.screen = genLabel(self, "screen", (0, BASE2, W, BASE2), "0")
        self.screen.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        #! buttons ==========================================
        def genBtn(window, id, rect, caption, func=None, pclass=None):
            btn = QPushButton(window)
            btn.setObjectName(id)
            btn.setGeometry(*rect)
            btn.setText(caption)
            if func:
                btn.clicked.connect(func)
            if pclass:
                btn.setProperty('class', pclass)
            return btn

        genfunc = lambda ch: lambda: self.btnPressed(ch)
        
        self.btn["close"] = genBtn(self, "close", (W-BASE, 0, BASE, BASE), "X", self.terminate)
        for i, row in enumerate(self.calculator.keyboard):
            for j, char in enumerate(row):
                self.btn[char] = genBtn(self, char, (BASE2*j, BASE2*(i+2), BASE2, BASE2), char, genfunc(char), 'keyboard')

        self.show()

    #! events ==============================================
    def btnPressed(self, key):
        # logger(f'Button "{key}" was pressed.')
        try:
            res=self.calculator.action(key)
        except ZeroDivisionError:
            self.screen.setText('Divided by 0')
            return
        if res:
            self.subscreen.setText(res[0])
            self.screen.setText(res[1])

    def terminate(self):
        self.close()
        logger("Terminating.")

    # move window ==============================================
    def mousePressEvent(self, event):
        if event.button() == 1: # Qt.LeftButton=1
            self.m_Position = event.globalPos()-self.pos()
            if self.m_Position in self.title.geometry():
                self.m_flag = True
                self.setCursor(QCursor(Qt.CrossCursor))
                cur = event.globalPos()
                # logger("Window start moving from (%i,%i)" % (cur.x(), cur.y()))
            else:
                del self.m_Position
            event.accept()

    def mouseMoveEvent(self, event):
        if self.m_flag:
            self.move(event.globalPos()-self.m_Position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if self.m_flag:
            self.m_flag = False
            self.setCursor(QCursor(Qt.ArrowCursor))
            cur = event.globalPos()
            # logger("Window stopped moving at (%i,%i)" % (cur.x(), cur.y()))

class BasicCalculator:
    operations={
        '':lambda a,b:b,
        '+':lambda a,b:a+b,
        '−':lambda a,b:a-b,
        '×':lambda a,b:a*b,
        '÷':lambda a,b:a/b if a%b else a//b,
        '%':lambda a,b:a%b,
        '=':lambda a,b:b or a,
    }

    keyboard = [
        ['C/AC', 'BS', '%', '÷'],
        ['7', '8', '9', '×'],
        ['4', '5', '6', '−'],
        ['1', '2', '3', '+'],
        [' ', '0', '.', '=']
    ]

    def __init__(self):
        self.storedNumber=0
        self.state=''
        self.temp=''
        self.showSubscreen=False
    
    @property
    def getTemp(self):
        p=0 if not self.temp else float(self.temp) if '.' in self.temp else int(self.temp)
        self.temp=''
        self.showSubscreen=True
        return p

    def action(self,key):
        # keys: ['C/AC', 'BS', '%', '÷', '×', '−', '+', '=']
        if key.isdigit():
            self.temp=key if self.temp=='' else self.temp+key
        elif key=='.':
            if '.' not in self.temp:
                self.temp+='.' if self.temp else '0.'
            else:
                return
        elif key in {'+','−','×','÷','%'}:
            if self.state=='=':
                self.storedNumber=self.getTemp or self.storedNumber
            else:
                self.storedNumber=self.operations[self.state](self.storedNumber,self.getTemp) if self.temp else self.storedNumber 
            self.state=key
        elif key == '=':
            self.storedNumber=self.operations[self.state](self.storedNumber,self.getTemp)
            self.showSubscreen=False
            self.state='='
            logger(f'result: {self.storedNumber}')
            return '',nFormat(self.storedNumber)
        elif key == 'C/AC':
            if self.temp:
                self.temp=''
            else:
                self.__init__()
        elif key == 'BS':
            self.temp='' if len(self.temp)==1 else self.temp[:-1]
        else:
            return 
        return nFormat(self.storedNumber) if self.showSubscreen else '', (self.state if self.state!='=' else '')+(self.temp if self.temp else '0')

def main():
    app = QApplication(argv)
    ex = MainWindow(BasicCalculator(),"Furculator - basic")
    exit(app.exec_())

if __name__ == "__main__":
    main()
