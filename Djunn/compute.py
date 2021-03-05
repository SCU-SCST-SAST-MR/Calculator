import math
import re
# import sin, cos, sqrt, log
PI = 3.141592653589793
E = 2.718281828459045

def myCos(n):
    return math.cos(n)

def mySin(n):
    return math.sin(n)

def mySqrt(n):
    if n<0:
        raise ValueError(r'math domain error')
    return n**(1/2)

def myLog(n):
    return math.log(n) 

# 数学表达式运算函数 
def getPostfixExp(inExp):
    # 数字越大优先级越高
    priority = {'*':2,'/':2,'+':1,'-':1,'(':0}
    stack,res,temp=[],[],[]
    for c in inExp+' ': # 不加空格有可能访问不了最后的字符
        if c.isdigit() or c=='.':
            temp.append(c)
            continue
        if temp: # 处理连续的数字
            res.append(''.join(temp))
            temp.clear()
        if c in priority.keys() and c!='(' and c!=')':
            if not stack:
                stack.append(c)
            else:
                while stack:
                    if priority[stack[-1]] >= priority[c]:
                        res.append(stack.pop())
                    else:
                        break
                stack.append(c)
        elif c=='(':
            stack.append(c)
        elif c==')':
            while stack:
                t = stack.pop()
                if(t=='('):
                    break
                else:
                    res.append(t)

    while stack:
        res.append(stack.pop())
    print(res)
    return res

# 计算后缀表达式
def calculate(postExp):
    opt = {
        '-': lambda x,n: x.pop() - n,
        '+': lambda x,n: x.pop() + n,
        '*': lambda x,n: x.pop() * n,
        '/': lambda x,n: x.pop() / n,
    }
    stack = []
    for n in postExp:
        # print(stack)
        if n.isdigit() or '.'in n:
            stack.append(float(n))
            if len(postExp)==1:
                return n
        elif n in opt.keys():
            num = stack.pop()
            res = opt[n](stack,num)
            stack.append(res)
    
    return res

def factorial(exp1,exp2=None): # 阶乘函数
    if '.' in exp1 or '-' in exp1 or exp2:
        raise ValueError('illegal expression')
    if exp1=='0' or exp1=='1':
        return '1'
    if int(exp1) > 101: #超过101!就会显示不完整
        raise ValueError('number is too big')
    res = 1
    for i in range(1,int(exp1)+1):
        res *= i
    return ' '+str(res)+' '

def replace(exp): #将表达式替换为eval认识的
    dic = {'ln':'log', 'E':str(math.e), 'Pi':str(math.pi),}
    #print('gp0:',exp.group(0))
    if exp.group(0) in dic.keys():
        return dic[exp.group(0)]
    elif '^' in exp.group(0):
        return '**'
    elif '!' in exp.group(0):
        t = exp.group(0).split('!')
        return factorial(*exp.group(0).split('!'))

def myEvalTemp(expr):
    exceptList=['cos','sin','log','sqrt','**'] # 目前无法处理
    if not expr:
        raise ValueError('illegal expression')
    for eLst in exceptList:
        if eLst in expr:
            res = eval(expr)
            return res
    try:
        exp=re.sub(r'ln|E|Pi|\-?\d+(.\d+)?\!|\^',replace,expr)
        print('exp==',exp)
        res = calculate(getPostfixExp(exp))
    except BaseException:
        raise SyntaxError('illegal expression')
    return res
    
# 以下为测试用代码
if __name__=='__main__': 
    # pst=getPostfixExp('10+10*(3-2)+1*3+4')
    # print('pst'+str(pst))
    # res=calculate(pst)
    # print(res)
    # print(myEvalTemp('1+2 * 3 / 4 +100'))
    pstt = '1.1+1.2'
    print(myEvalTemp(pstt))