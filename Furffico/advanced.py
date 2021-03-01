
import time
from PyQt5.Qt import QCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from compute import Node,Rational,constants,Warning

#! UI ==============================================================
BASE = 30

def logger(event: str, pre=""):
    print(pre+time.strftime("[%Y-%m-%d %H:%M:%S] ",
                            time.localtime())+event.replace('\n', '\\n'))

def tostr(n):
    s=f'{n:.10}'.replace('e','𝐞') if isinstance(n,float) else str(n)
    return '-'+s[1:] if n<0 else s


class MainWindow(QMainWindow):
    subkeyboard = [
        ['(', ')', ''],
        ['sin', 'cos', 'tan'],
        ['asin', 'acos', 'atan'],
        ['sqrt', '^2', '^'],
        ['ln','log10','log2'],
        ['fact','perm','comb'],
        ['sum', 'avg', 'var'],
        ['π', '𝑒', 'φ'],
    ]
    keyboard = [
        ['AC', 'BS', '%', '÷'],
        ['7', '8', '9', '×'],
        ['4', '5', '6', '-'],
        ['1', '2', '3', '+'],
        [',', '0', '.', '=']
    ]

    tooltips={
        'AC':"全部清空",
        'BS':"退格",
        '%':"取余", # 好吧我知道%在大多数人眼中都是百分号
        '÷':'求商',
        '×':'求积',
        '-':'求差',
        '+':'求和',
        'sin':"sin(x):求x（弧度）的正弦",
        'cos':"cos(x):求x（弧度）的余弦",
        'tan':'tan(x):求x（弧度）的正切',
        'asin':'asin(x) x∈[-1,1]:求x的反正弦（弧度）',
        'acos':'acos(x) x∈[-1,1]:求x的反余弦（弧度）',
        'atan':'atan(x):求x的反正切（弧度）',
        'sqrt':'sqrt(x) x>0:求x的平方根',
        '^2':"x^2:求x的平方",
        '^':"x^y:求x的y次幂",
        'ln':'ln(x) x>0:求x的自然对数',
        'log10':'log10(x) x>0:求以10为底的x的对数',
        'log2':'log2(x) x>0:求以2为底的x的对数',
        'fact':'fact(n) n∈<b>N</b>:求n的阶乘',
        'perm':'perm(n,k) n,k∈<b>N</b> 0≤k≤n:求从n个相异元素中取出k个元素，k个元素的排列数量',
        'comb':'comb(n,k) n,k∈<b>N</b> 0≤k≤n:求从n个相异元素中取出k个元素，k个元素的组合数量',
        'sum':'sum(x1,x2,...,xn):求x1+x2+...+xn',
        'avg':'avg(x1,x2,...,xn):求x1,x2,...,xn的平均值',
        'var':'var(x1,x2,...,xn):求x1,x2,...,xn的方差',
        'π':'圆周率',
        '𝑒':'自然对数的底',
        'φ':'黄金分割比', # 凑数用的
    }

    def __init__(self, title):
        logger("Initializing.")
        super().__init__()
        self.windowtitle = title
        self.UIinit()
        self._text = ''
        self._subtext = ''
        self.clearscreen = False
        self.result=0
        logger("Initialized.")

    def UIinit(self):
        self.btn = {}
        self.m_flag = False
        BASE2 = BASE*2
        #! window ===========================================
        W, H = BASE2*(max(map(len, self.keyboard))+max(map(len,
                                                           self.subkeyboard))), BASE2*(2+len(self.keyboard))
        self.setFixedSize(W, H)
        self.setWindowFlag(2048)  # Qt.FramelessWindowHint=2048
        self.setAttribute(120, True)  # Qt.WA_TranslucentBackground=120
        # 好像样式表不能和程序一起打包呢、、、只好写进程序了
        self.setStyleSheet("*{color:#000;font-family:Consolas;border:0;padding:5px 2px 5px 2px;background:rgba(230,230,230,.8)}QLabel#title{font-size:15px}QLabel#subscreen{font-size:20px;padding-right:5px}QLabel#screen{font-size:25px;border-bottom:1px solid #e6e6e6}QPushButton.subkeyboard{font-size:16px}QPushButton.keyboard{font-size:24px}QPushButton.keyboard:hover,QPushButton.subkeyboard:hover{background:#e6e6e6}QPushButton#close{background:rgba(247,188,196,.8);font-size:15px}QPushButton#close:hover{background:#f7bcc4}")

        #! labels ===========================================
        def genLabel(window, id, rect, caption, pclass=None):
            lb = QLabel(window)
            lb.setGeometry(*rect)
            lb.setText(caption)
            lb.setObjectName(id)
            if pclass:
                lb.setProperty('class', pclass)
            return lb

        self.title = genLabel(
            self, "title", (0, 0, W-BASE, BASE), self.windowtitle)
        self.subscreen = genLabel(self, "subscreen", (0, BASE, W, BASE), "")
        self.subscreen.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.screen = genLabel(self, "screen", (0, BASE2, W, BASE2), "")
        self.screen.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        #! buttons ==========================================
        def genBtn(window, id, rect, caption, func=None, pclass=None,tooltip=''):
            btn = QPushButton(window)
            btn.setObjectName(id)
            btn.setGeometry(*rect)
            btn.setText(caption)
            if func:
                btn.clicked.connect(func)
            if pclass:
                btn.setProperty('class', pclass)
            if tooltip:
                btn.setToolTip(tooltip)
            return btn

        genfunc = lambda ch: lambda: self.btnPressed(ch)

        self.btn["close"] = genBtn(
            self, "close", (W-BASE, 0, BASE, BASE), "X", self.terminate)
        rb = BASE2*max(len(i) for i in self.subkeyboard)
        genLabel(self, 'fill', (0, BASE2*2, rb, BASE2), '')
        for i, row in enumerate(self.subkeyboard):
            for j, char in enumerate(row):
                self.btn[char] = genBtn(self, char, (BASE2*j, BASE*(i+6), BASE2, BASE), char, genfunc(char), 'subkeyboard', self.tooltips.get(char,''))
        for i, row in enumerate(self.keyboard):
            for j, char in enumerate(row):
                self.btn[char] = genBtn(self, char, (BASE2*j+rb, BASE2*(i+2), BASE2, BASE2), char, genfunc(char), 'keyboard', self.tooltips.get(char,''))

        self.show()

    #! properties ============================================
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, s):
        if isinstance(s, str):
            self._text = s
        else:
            self._text = str(s)
        self.screen.setText(self._text)

    @property
    def subtext(self):
        return self._text

    @subtext.setter
    def subtext(self, s):
        if isinstance(s, str):
            self._subtext = s
        else:
            self._subtext = str(s)
        self.subscreen.setText(self._subtext)

    #! events ==============================================
    def btnPressed(self, key):
        # logger(f'Button "{key}" was pressed.')
        if self.clearscreen:
            if key == '=':
                if isinstance(self.result,Rational) and not self.result.isint():
                    self.text = '=' + tostr(float(self.result))
                return
            elif key in ['+','-','×','÷','%','^','^2']:
                self.text = tostr(self.result) + key
                self.subtext = ''
                self.clearscreen = False
                return
            self.text = self.subtext = ''
            self.clearscreen = False
        if not key:
            pass
        elif key == 'AC': # 清空
            self.text = self.subtext = ''
        elif key == 'BS': # 退格
            self.text = self.text[:-1] if self.text else ''
        elif key == '=':  # 计算
            logger('Received infix-expression '+self.text)
            try:
                tree = Node.parseInfixexp(self.text)
                logger('Converted into '+repr(tree))
                result = tree.evaluate()
                logger('Result: '+tostr(result))
                self.text, self.subtext = '=' + tostr(result), self.text
            except Warning as e:
                logger(str(e))
                self.text, self.subtext = e.msg, self.text
            except OverflowError as e:
                logger(str(e))
                self.text, self.subtext = 'number overflowed', self.text
            except Exception as e:
                logger(str(e))
                self.text, self.subtext = 'Error occurred', self.text
            else:
                self.result=result
            self.clearscreen = True
        elif key in '0123456789.+-×÷%^2),(':
            self.text = self.text+key
        elif key in constants.keys():
            self.text = self.text+key
        else: # 函数自动补左括号
            self.text = self.text+key+'('

    def terminate(self):
        self.close()
        logger("Terminating.")

    # move window ==============================================
    def mousePressEvent(self, event):
        if event.button() == 1:  # Qt.LeftButton=1
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

def main():
    from sys import exit,argv
    app = QApplication(argv)
    ex = MainWindow("Calculator - advanced")
    exit(app.exec_())

if __name__ == "__main__":
    main()