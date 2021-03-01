## 说明

打包后的程序见[./dist](dist)

三种模式：命令行（无gui），基础（有gui），高级（有gui~~，其实不高级，只是给第一个套了个皮~~）

高级模式和命令行模式的特性：
- 中用的数学函数都是通过泰勒展开或者二分法实现的，整个程序都没有调用python的标准库math；
- 分数的实现和应用（基于python的重载运算符）。
  - （对于整数和整数的除法，大概率会返回一个分数作为结果，如果需要浮点数结果再按一下等号就好了。）
- 鼠标悬停在部分按钮上可以看到使用说明。

双击图标打开时默认为高级模式，若想康康其余两个模式请通过命令行运行并加上参数，如。

```
命令行模式： .\dist\calculator.exe cmd
基础模式：  .\dist\calculator.exe basic
```

如果想要用python运行程序，需要经过以下步骤：

```
#创建并切换到虚拟环境
# 1.powershell
> python -m venv .\venv
> .\venv\Scripts\activate
# 2.bash
$ python3 -m venv ./venv
$ source ./venv/bin/activate

#安装依赖
pip install -r requirements.txt

#运行程序
# 1.高级模式（二者皆可）
python calculator.py
python advanced.py
# 2.命令行模式（二者皆可）
python calculator.py cmd
python compute.py
# 3.基础模式（二者皆可）
python calculator.py basic
python basic.py
```

不足：
- GUI不好看（抱歉在下在这方面实在是没有什么天赋，但又想搞点扁平化的东西）；
- 代码有点乱；
- bug应该还挺多的；
- 肯定还有

以上。

by Furffico