import operator
from functools import lru_cache,reduce

PI=3.14159265358979323846264338327950288419716939937510582
E=2.718281828459045

#! Warnings ================================================================
class Warning(BaseException):
    def __init__(self, message, *args):
        if not args:
            super().__init__(message)
        else:
            super().__init__(*args)
        self.msg = message

#! Number Types ===================================================================
class Rational:
    def __init__(self, numerator: int, denominator: int = 1):
        if denominator == 0:
            raise Warning('divided by zero')
        if numerator == 0:
            self.numerator = 0
            self.denominator = 1
        else:
            self.numerator = numerator*sgn(denominator)
            self.denominator = abs(denominator)
            self.reduce()

    def reduce(self):
        gcd = GCD(abs(self.numerator), self.denominator)
        self.numerator //= gcd
        self.denominator //= gcd

    def __str__(self):
        if self.denominator != 1:
            return '{}/{}'.format(self.numerator, self.denominator)
        else:
            return '{}'.format(self.numerator)

    def __float__(self):
        return self.numerator/self.denominator
    
    def __int__(self):
        return self.numerator//self.denominator

    __repr__ = __str__

    #! 一元运算符 ===========================================
    def __neg__(self):
        return Rational(-self.numerator, self.denominator)

    def __pos__(self):
        return self

    def reciprocal(self):
        return Rational(self.denominator, self.numerator)
    
    def __abs__(self):
        return Rational(abs(self.numerator), self.denominator)
    
    def __hash__(self):
        return hash((self.numerator,self.denominator))

    #! 二元运算符 ===========================================
    def __add__(a, b):
        if isinstance(b, Rational):
            return Rational(a.numerator*b.denominator+b.numerator*a.denominator, a.denominator*b.denominator)
        elif isinstance(b, int):
            return Rational(a.numerator+b*a.denominator, a.denominator)
        else:
            return float(a)+b

    def __sub__(a, b):
        if isinstance(b, Rational):
            return Rational(a.numerator*b.denominator-b.numerator*a.denominator, a.denominator*b.denominator)
        elif isinstance(b, int):
            return Rational(a.numerator-b*a.denominator, a.denominator)
        else:
            return float(a)-b

    def __rsub__(a, b):
        if isinstance(b, Rational):
            return Rational(-a.numerator*b.denominator+b.numerator*a.denominator, a.denominator*b.denominator)
        elif isinstance(b, int):
            return Rational(-a.numerator+b*a.denominator, a.denominator)
        else:
            return -float(a)+b

    def __mul__(a, b):
        if isinstance(b, Rational):
            return Rational(a.numerator*b.numerator, a.denominator*b.denominator)
        elif isinstance(b, int):
            return Rational(a.numerator*b, a.denominator)
        else:
            return float(a)*b

    def __truediv__(a, b):
        if isinstance(b, Rational):
            return Rational(a.numerator*b.denominator, b.numerator*a.denominator)
        elif isinstance(b, int):
            return Rational(a.numerator, a.denominator*b)
        else:
            return float(a)/b

    def __rtruediv__(a, b):
        if isinstance(b, Rational):
            return Rational(b.numerator*a.denominator, a.numerator*b.denominator)
        elif isinstance(b, int):
            return Rational(a.denominator*b, a.numerator)
        else:
            return b/float(a)

    def __pow__(a, b):
        if isinstance(b, int):
            return Rational(a.denominator**b, a.numerator**b)
        else:
            return float(a)**float(b)
    
    def __rpow__(a, b):
        return b**float(a)

    def __mod__(a, b):
        if isinstance(b, Rational):
            return Rational((a.numerator*b.denominator) % (b.numerator*a.denominator), a.denominator*b.denominator)
        elif isinstance(b, int):
            return Rational(a.numerator % (b*a.denominator), a.denominator)
        else:
            return float(a) % b
    
    #! 关系运算符====================================================
    def __eq__(a, b):
        if isinstance(b, Rational):
            return a.numerator==b.numerator and a.denominator==b.numerator
        elif isinstance(b, int):
            return a.numerator==b if a.isint() else False
        else:
            return float(a)==float(b)
    def __gt__(a, b):
        return float(a)>float(b)
    def __ge__(a, b):
        return float(a)>=float(b)
    def __lt__(a, b):
        return float(a)<float(b)
    def __le__(a, b):
        return float(a)<=float(b)
    

    __radd__ = __add__
    __rmul__ = __mul__

    def isint(self):
        return self.denominator == 1

def isint(n):
    return isinstance(n,int) or isinstance(n,Rational) and n.isint()

#! Math================================================================

def infSumSeries(a,pre=None,post=None,precision=1e-12,specials={}):  # 计算无穷数项级数
    prefunc=pre or (lambda x:x)
    postfunc=post or (lambda x:x)
    for n,value in specials.items():
        specials[float(n)]=value
    def wrapped(x):
        if x in specials:
            return float(specials[x])
        x=prefunc(float(x))
        result=count=0
        for n in range(0,10000):
            cur=a(n,x)
            result+=cur
            if cur==0 or abs(cur)<precision*abs(result):
                count+=1
                if count>5:
                    break
            elif count:
                count=0
        else:
            raise ValueError('Series converages too slow')
        return postfunc(result)
    return wrapped

def bisection(up,bottom,func,target=0,precision=1e-12): # 二分法求零点
    delta=up-bottom
    upvalue=func(up)-target
    btvalue=func(bottom)-target
    if (_:=sgn(upvalue)*sgn(btvalue))>0:
        raise ValueError()
    elif _==0:
        return up if upvalue==0 else bottom
    while up-bottom>precision*abs(bottom):
        midvalue=func(mid:=(up+bottom)/2)-target
        if sgn(upvalue)*sgn(midvalue)<0:
            btvalue,bottom=midvalue,mid
        elif midvalue==0:
            return mid
        else:
            upvalue,up=midvalue,mid
    return (up+bottom)/2

def domainWrapper(func,domain):
    def wrapped(*x):
        if domain(*x):
            return func(*x)
        else:
            raise Warning(f'Domain error')
    return wrapped

def oddeven(n):
    return -1 if n%2 else 1

def sgn(x):
    return 1 if x > 0 else 0 if x == 0 else -1
    
def GCD(a, b):
    if a < b:
        a, b = b, a
    while b:
        a, b = b, a % b
    return a

@lru_cache(maxsize=32)
def pow(x,n):
    if isint(n) and n>0:
        return x if n==1 else x*pow(x,n-1)
    return x**n

@lru_cache(maxsize=20000)
def seqFact(up,bottom=1,step=1):
    if up<=bottom:
        return 1
    else:
        return up*seqFact(up-step,bottom,step)

class Mathematical:
    div=lambda a, b: Rational(a, b) if isinstance(a, int) and isinstance(b, int) else a/b
    sqrt=domainWrapper(lambda x:x**0.5,lambda x:x>=0)
    sin=infSumSeries(lambda m,x:oddeven(m)*pow(x,2*m+1)/seqFact(2*m+1),lambda x:x%(2*PI),specials={0:0})
    cos=infSumSeries(lambda m,x:oddeven(m)*pow(x,2*m)/seqFact(2*m),lambda x:x%(2*PI),specials={0:1,0.0:1})
    tan=lambda x:Mathematical.sin(x)/Mathematical.cos(x)
    asin=domainWrapper(infSumSeries(lambda m,x:seqFact(2*m-1,1,2)/seqFact(m)/2**m/(2*m+1)*pow(x,2*m+1),specials={0:0,1:PI/2,-1:-PI/2}),lambda x:-1<=x<=1)
    acos=lambda x:PI/2-Mathematical.asin(x)
    _atan1=infSumSeries(lambda m,x:oddeven(m)*pow(x,2*m+1)/(2*m+1))
    _atan2=infSumSeries(lambda m,x:oddeven(m-1)/pow(x,2*m+1)/(2*m+1))
    atan=lambda x: Mathematical._atan1(x) if abs(x)<1 else Mathematical._atan2(x)+sgn(x)*PI/2 if abs(x)>1 else sgn(x)*PI/4
    exp=lambda x:E**x
    ln=domainWrapper(lambda x: bisection(2*x**0.5-2,1-1/x,Mathematical.exp,x) if x!=1 else 0,lambda x:x>0)
    log10=lambda x:Mathematical.ln(x)/2.302585092994046
    log2=lambda x:Mathematical.ln(x)/0.6931471805599453
    fact=domainWrapper(lambda x:reduce(operator.mul,range(1,x+1),1),lambda x:isint(x) and x>=0)
    perm=domainWrapper(lambda n,k:reduce(operator.mul,range(n,n-k,-1),1),lambda n,k: isint(n) and isint(k) and 0<=k<=n)
    comb=lambda n,k:Rational(Mathematical.perm(n,k),Mathematical.fact(k))


class Statistical:
    def sum(*data):
        return sum(data)

    def average(*data):
        return sum(data)/len(data)

    def variance(*data):
        avg = Statistical.average(*data)
        return sum([(i-avg)**2 for i in data])/len(data)

#!comupting =====================================================
class MyIterator:
    def __init__(self, s):
        self.string = s
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.string):
            raise StopIteration()
        char = self.string[self.index]
        self.index += 1
        return char

    def last(self):
        if self.index:
            self.index -= 1

    def subiter(self, end, start=None):
        if start:
            while 1:
                char = next(self)
                if start(char):
                    self.last()
                    break
        while 1:
            try:
                char = next(self)
            except StopIteration:
                return
            if end(char):
                self.last()
                break
            else:
                yield char

    def safenext(self):
        try:
            return self.__next__()
        except StopIteration:
            return ''
    
    def safelast(self):
        return self.string[self.index-1] if self.index else ''

class Token:
    def __init__(self,t,value,neg=False):
        self.t=t # num,op,func,lb,rb,sgn,const
        if t=='num':
            self.neg=False
            self.v=Number(('-'if neg else '')+value)
        elif t=='const':
            self.neg=False
            if neg:
                self.v=Node('-',[0,constants[value]])
            else:
                self.v=constants[value]
        elif t=='func' and neg:
            value.neg=True
            self.v=value
            self.neg=False
        else:
            self.v=value
            self.neg=neg

    def __repr__(self):
        return f'<{self.t}:{"-" if self.neg else ""}{self.v}>'

def tokenizing(expr):
    readin = MyIterator(expr)
    tokens=[]
    def attach(t,v):
        if tokens and tokens[-1].t=='sgn':
            tokens[-1]=Token(t,v,tokens[-1].v=='-')
        else:
            tokens.append(Token(t,v))
    for char in readin:
        if char in '0123456789.':
            value = char + ''.join(readin.subiter(lambda c: c not in '0123456789.'))
            attach('num',value)
        elif char in constants.keys():
            attach('const',char)
        elif char in '+-':
            if tokens and tokens[-1].t in {'num','func','rb'}:
                tokens.append(Token('op',char))
            else:
                tokens.append(Token('sgn',char))
        elif char in operands:
            tokens.append(Token('op',char))
        elif char == '(':
            attach('lb','(')
        elif char == ')':
            tokens.append(Token('rb',')'))
        elif char.isalpha():
            value = char+''.join(readin.subiter(lambda c: not c.isalnum()))
            if value not in funcdict:
                raise Warning('illegal expression')
            if readin.safenext() == "(":  # 将函数调用看作一个整体来处理
                layer, param, temp = 0, [], ''
                for i in readin:
                    if i == ',' and not layer:
                        param.append(temp)
                        temp = ''
                    elif i == '(':
                        layer += 1
                        temp += i
                    elif i == ')':
                        if layer:
                            layer -= 1
                            temp += i
                        else:
                            break
                    else:
                        temp += i
                param.append(temp)
            attach('func',Node(value, [Node.parseInfixexp(i) for i in param]))
        else:
            raise Warning('illegal expression')
    return tokens

class Number:
    def __init__(self, n,neg=False):
        if isinstance(n, str):
            self.value = float(n) if '.' in n or 'e' in n else int(n)
        elif isinstance(n, (int, float)):
            self.value = n
        else:
            raise ValueError()
        self.neg=neg

    def __repr__(self):
        return ('-' if self.neg else '')+str(self.value)

    def evaluate(self):
        return self.value*(-1 if self.neg else 1)

class Constant(Number):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return self.name
    
    def evaluate(self):
        return self.value

class Node:
    def __init__(self, name, params=None,neg=False):
        self.name = name
        self.params = params or []
        self.neg=neg

    def addpara(self, parameter):
        self.params.append(parameter)

    def __repr__(self):
        return '{}{}({})'.format('-' if self.neg else '',self.name, ', '.join(map(repr, self.params)))

    def evaluate(self):
        for index, child in enumerate(self.params):
            if isinstance(child, (Node, Number)):
                self.params[index] = child.evaluate()
        return funcdict[self.name](*self.params)*(-1 if self.neg else 1)

    @staticmethod
    def parseInfixexp(expr):
        tokeniter=MyIterator(tokenizing(expr))
        priority={'+':1,'-':1,'×':2,'*':2,'÷':2,'/':2,'%':2,'^':3,'𝐞':4,'(':0}
        stack, output = [], []
        def shunting():
            try:
                output.append(Node(stack.pop().v, [output.pop(), output.pop()][::-1]))
            except IndexError:
                raise Warning('illegal expression')
        
        for i in tokeniter:
            if i.t in {'num','func','const'}:
                output.append(i.v)
            elif i.t=='op':
                while stack and priority[stack[-1].v] >= priority[i.v]:
                    shunting()
                stack.append(i)
            elif i.t=='lb':
                stack.append(i)
            elif i.t=='rb':
                while stack and stack[-1].t != 'lb':
                    shunting()
                try:
                    br=stack.pop()
                except IndexError:
                    raise Warning('brackets do not match')
                else:
                    if br.neg:
                        output[-1].neg=True
            else:
                raise Warning('illegal expression')
        while stack:
            shunting()
        return output[0]

#!definition ==========================================================
operands={'+','-','×','*','÷','/','%','^','𝐞'}

funcdict = {
    '+': operator.add,
    '-': operator.sub,
    '×': operator.mul,
    '÷': Mathematical.div,
    '%': operator.mod,
    '^': operator.pow,
    'sqrt': Mathematical.sqrt,
    'sin': Mathematical.sin,
    'cos': Mathematical.cos,
    'tan': Mathematical.tan,
    'asin': Mathematical.asin,
    'acos': Mathematical.acos,
    'atan': Mathematical.atan,
    'exp':Mathematical.exp,
    'ln':Mathematical.ln,
    'log10':Mathematical.log10,
    'log2':Mathematical.log2,
    'fact':Mathematical.fact,
    'perm':Mathematical.perm,
    'comb':Mathematical.comb,
    'sum': Statistical.sum,
    'avg': Statistical.average,
    'var': Statistical.variance,
    # assistive
    '𝐞': lambda a,b:a*10**b,
    '*': operator.mul,
    '/': Mathematical.div,
}

constants = {
    'π': Constant('π', PI),
    '𝑒': Constant('𝑒', E),
    'φ': Constant('φ',1.618033988749895)
}

def main():
    print('Press Ctrl-C to terminate this program.')
    print('Type "help" for a useless help.')
    try:
        while 1:
            s = input('> ')
            if not s:
                continue
            elif s=='help':
                print('Available operations:\n   ',end='')
                print(*funcdict,sep=', ')
                print('Available constants:\n   ',end='')
                print(*constants,sep=', ')
                print('   And please represent π,𝑒,φ with pi,E,phi.')
                continue
            else:
                s=s.replace('pi','π').replace('E','𝑒').replace('phi','φ')
                try:
                    tree = Node.parseInfixexp(s)
                    print('=', tree.evaluate())
                except Warning as e:
                    print(e.msg)
    except KeyboardInterrupt:
        print('\nProgram exited.')

if __name__ == "__main__":
    main()