# -*- coding: utf-8 -*-

"""
author : yydshmcl@outlook.com
Design date : 2022/3/12
"""

import webbrowser
import sys
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import *
import tkinter.colorchooser
import function.index
import api
from tkinter import ttk
import os
index = function.index

ver = index.parse("config/config.json").json()

root = tk.Tk()

def Sys():
    __data = os.name
    if __data =='nt':
        return '您的操作系统是Windows,异常检测：【无】'
    elif __data == 'java':
        return '您的运行环境是Java,异常检测：【无】'
    else:
        return '您的操作系统或者运行环境非Windows或Java，可能会出现部分未知错误,异常检测：【未知错误】'

FileTree = ttk.Treeview(root)
FTreeOne = FileTree.insert("", 0, "测试版", text="测试版，暂时无法显示文件树", values=("F1"))
FtreeTwo = FileTree.insert(FTreeOne,1,"cs",text="了解更多请访问官网！！！", values=("F2"))
FileTree.pack(side='left',anchor='w',fill='both')

lable_sys = tk.Label(root,text=Sys())
lable_sys.pack(side='top',anchor='w')#fill='both'

stickup = ""

textPad= ScrolledText(bg='white', height=10)
textPad.pack(fill=tk.BOTH, expand=1)
textPad.focus_set()

SetFile = index.parse("config").json()

def IDESetWind():
    winNew = tk.Toplevel(root)
    winNew.geometry('600x450+374+182')
    winNew.title('IDE设置')

    def SetBg(bg = "#000",fg = "#FFF") -> None:
        SetFile['Bg'] = bg
        SetFile['Fg'] = fg
        with open("config/set.json") as file:
            file.write(SetFile)
            file.close
        return None

    def bgcolor() -> str:
        BgColor = tkinter.colorchooser.askcolor()
        return BgColor
    bgButton = ttk.Button(winNew,text="选择背景色",command=bgcolor).pack()

def ConfigWind():
    winNew = tk.Toplevel(root)
    winNew.geometry('600x450+374+182')
    winNew.title('参数设置')
    hj_path = ""
    PathLab = ttk.Label(winNew,text=sys.path[5]+"\\python.exe",relief='solid').grid(row=0,column=1,columnspan=2)
    PathBtn = ttk.Button(winNew,text="更改解释器路径").grid(padx=0,row=0,column=0)
    DabaoBtn = ttk.Button(winNew,text="打包项目").grid(padx=0,row=1,column=0)

def FileSetWind():
    winNew = tk.Toplevel(root)
    winNew.geometry('600x450+374+182')
    winNew.title('文件设置')

def NewFile():  #新文件
    textPad.delete(1.0,tk.END)

def GetFile(): #读取文件
    filename = askopenfilename(defaultextension='.py')
    if filename != '':
        textPad.delete(1.0,tk.END)#delete all
        f = open(filename,'r',encoding='utf-8',errors='ignore')
        textPad.insert(1.0,f.read())
        f.close()

def SaveFile(**kages): #另存文件
    filename = asksaveasfilename(initialfile = 'new',defaultextension ='.py')
    if filename != '':
        fh = open(filename,'w',encoding='utf-8',errors='ignore')
        msg = textPad.get(1.0,tk.END)
        fh.write(msg)
        fh.close()

def EXEInfo():
    winNew = tk.Toplevel(root)
    winNew.geometry('600x450+374+182')
    winNew.title('软件信息')
    lb = tk.Label(winNew,text=f'软件版本 : {ver["ExeVer"]}',relief='solid').pack()
    lb2 = tk.Label(winNew,text=f'核心版本 : {ver["version"]}',relief='solid').pack()
    lb3 = tk.Label(winNew,text=f'当前主题 : {ver["topic"]}',relief='solid').pack()
    lb4 = tk.Label(winNew,text=f'贡献者 : {ver["contributors"]}',relief='solid').pack()
    lb5 = tk.Label(winNew,text=f'源码托管平台 : {ver["platform"]}',relief='solid').pack()

def Plugin():
    winNew = tk.Toplevel(root)
    winNew.geometry('600x450+374+182')
    winNew.title('插件')
    lb = tk.Label(winNew,text=f'已安装插件列表').pack()
    lb2 = tk.Label(winNew,text=f'{api.alert().GetPlugin()}',relief='solid').pack()

def showPopoutMenu(w, menu):
    def popout(event):
        menu.post(event.x + root.winfo_rootx(), event.y + root.winfo_rooty()) 
        root.update() 
    root.bind('<Button-3>', popout) 

#为控制台设置一个容器
frame2=tk.LabelFrame(root,text='控制台',height=100)
frame2.pack(fill=tk.BOTH, expand=1)

global textMess

class Stdout():	# 重定向类
    def __init__(self):
    	# 将其备份
        self.stdoutbak = sys.stdout		
        self.stderrbak = sys.stderr
        # 重定向
        sys.stdout = self
        sys.stderr = self

    def write(self, info):
        # info信息即标准输出sys.stdout和sys.stderr接收到的输出信息
        textMess.insert('end', info)# 在多行文本控件最后一行插入print信息
        textMess.update()# 更新显示的文本，不加这句插入的信息无法显示
        textMess.see(tk.END)# 始终显示最后一行，不加这句，当文本溢出控件最后一行时，不会自动显示最后一行

    def restoreStd(self):
        # 恢复标准输出
        sys.stdout = self.stdoutbak
        sys.stderr = self.stderrbak
mystd = Stdout()

#放置一个文本框作为信息输出窗口
textMess= ScrolledText(frame2,bg='white', height=10,cursor="arrow")
textMess.pack(fill=tk.BOTH, expand=1)
##清空信息窗
def clearMess():
    global textMess
    textMess.delete(1.0,tk.END)

#用户输出信息
def myprint(txt):
    global textMess
    if textMess != None :
        textMess.insert(tk.END, txt)
        textMess.see(tk.END)

#输出彩色信息
def colorprint(txt,color='black'):
    global textMess
    if textMess != None :
        if color!='black':
            textMess.tag_config(color, foreground=color)   
        textMess.insert(tk.END, txt,color)
        textMess.see(tk.END)

#运行用户程序
def runpy():
    global textPad,textMess
    try:
        msg = textPad.get(1.0,tk.END)
        mg=globals()
        ml=locals()
        exe = exec(msg,mg,ml)
        Stdout.write(exe)
    except Exception as e:
        colorprint('\n[error]:'+str(e)+'\n','red')

def no():
    answer = tk.messagebox.askokcancel('该功能正在制作中','选择确定查看详情，选择取消关闭弹窗')
    if answer:
        webbrowser.open('https://github.com/Buelie/Machine')
    else:
        pass

def yhxy():
    winNew = tk.Toplevel(root)
    winNew.geometry('600x450+374+182')
    winNew.title("用户协议")
    f = "The MIT License (MIT)\
\nCopyright (c) 2023  |  yydshmcl@outlook.com\
\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”),\n to deal in the Software without restriction, \nincluding without limitation the rights to use, \ncopy, modify, merge, publish, distribute, sublicense, \nand/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\
\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\
\nThe Software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability,\n fitness for a particular purpose and noninfringement. \nIn no event shall the authors or copyright \nholders be liable for any claim, damages or other liability, \nwhether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the Software."
    lable = tk.Label(winNew,text=f).pack()

StartEXE = ttk.Button(root,text="运行程序",command=runpy,width=100).pack()#,relief='solid'

#菜单栏
MenuBar = tk.Menu(root,bg="#000",fg="#FFF",relief='solid')

# 创建一个下拉菜单“文件”，然后将它添加到顶级菜单中
filemenu = tk.Menu(MenuBar, tearoff=False,bg="#000",fg="#FFF",relief='solid')
filemenu.add_command(label="打开", command=GetFile)
filemenu.add_command(label="保存", command=SaveFile)
filemenu.add_command(label="新建", command=NewFile)
filemenu.add_command(label="运行", command=runpy)
filemenu.add_separator()
filemenu.add_command(label="退出", command=root.quit)
MenuBar.add_cascade(label="文件", menu=filemenu)
 
# 创建另一个“编辑”下拉菜单，然后将它添加到顶级菜单中
EditMenu = tk.Menu(MenuBar, tearoff=False,bg="#000",fg="#FFF",relief='solid')
EditMenu.add_command(label="剪切", command=no)
EditMenu.add_command(label="拷贝", command=no)
EditMenu.add_command(label="粘贴", command=no)
MenuBar.add_cascade(label="编辑", menu=EditMenu)
 
# 创建另一个“设置”下拉菜单，然后将它添加到顶级菜单中
settingmenu = tk.Menu(MenuBar, tearoff=False,bg="#000",fg="#FFF",relief='solid')
settingmenu.add_command(label="参数设置", command=ConfigWind)
settingmenu.add_command(label="文件设置", command=FileSetWind)
settingmenu.add_command(label="IDE设置", command=IDESetWind)
MenuBar.add_cascade(label="设置", menu=settingmenu)

# 创建另一个“帮助”下拉菜单，然后将它添加到顶级菜单中
helptmenu = tk.Menu(MenuBar,tearoff=False,bg="#000",fg="#FFF",relief='solid')
helptmenu.add_command(label="关于我们", command=no)
helptmenu.add_command(label="获取帮助", command=no)
helptmenu.add_command(label="软件信息", command=EXEInfo)
helptmenu.add_command(label="用户协议",command=yhxy)
helptmenu.add_command(label="插件", command=Plugin)
MenuBar.add_cascade(label="帮助", menu=helptmenu)

menu_f = tk.Menu(FileTree,bg="#000",fg="#FFF",tearoff=False,relief='raised')
menu_f.add_cascade(label = '新建',command=no)
menu_f.add_cascade(label = '打开文件所在位置',command=no)
menu_f.add_cascade(label = '复制路径',command=runpy)
menu_f.add_cascade(label="重命名")
showPopoutMenu(FileTree,menu_f)

menu_f = tk.Menu(FileTree)

# 显示菜单
root.bind('<Control - s>',SaveFile)
root.bind('<F9>',runpy)
root.config(menu=MenuBar)

#窗口设置
root.iconphoto(True,tk.PhotoImage(file="image/cobweb.png"))
root.geometry("600x450+374+182")
root.title("清云IDE")
root.mainloop()

# pyinstaller
