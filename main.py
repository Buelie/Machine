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

index = function.index

root = tk.Tk()
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
        SetBg(BgColor)
        return BgColor
    bgButton = tk.Button(winNew,text="选择背景色",command=no).pack()

def FileSetWind():
    winNew = tk.Toplevel(root)
    winNew.geometry('600x450+374+182')
    winNew.title('文件设置')

def CSSetWind():
    winNew = tk.Toplevel(root)
    winNew.geometry('600x450+374+182')
    winNew.title('参数设置')

def NewFile():  #新文件
    textPad.delete(1.0,tk.END)

def GetFile(): #读取文件
    filename = askopenfilename(defaultextension='.py')
    if filename != '':
        textPad.delete(1.0,tk.END)#delete all
        f = open(filename,'r',encoding='utf-8',errors='ignore')
        textPad.insert(1.0,f.read())
        f.close()

def SaveFile(): #另存文件
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
    ver = index.parse("config/config.json").json()
    lb = tk.Label(winNew,text=f'软件版本 : {ver["ExeVer"]}').pack()
    lb2 = tk.Label(winNew,text=f'核心版本 : {ver["version"]}').pack()
    lb3 = tk.Label(winNew,text=f'当前主题 : {ver["topic"]}').pack()
    lb4 = tk.Label(winNew,text=f'贡献者 : {ver["contributors"]}').pack()
    lb5 = tk.Label(winNew,text=f'源码托管平台 : {ver["platform"]}').pack()

def Plugin():
    winNew = tk.Toplevel(root)
    winNew.geometry('600x450+374+182')
    winNew.title('插件')
    lb = tk.Label(winNew,text=f'已安装插件列表').pack()
    lb2 = tk.Label(winNew,text=f'{api.alert().GetPlugin()}').pack()

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

StartEXE = tk.Button(root,text="运行程序",command=runpy,height=1).pack(fill=tk.BOTH, expand=1)


#菜单栏
MenuBar = tk.Menu(root,bg="#000",fg="#FFF")

# 创建一个下拉菜单“文件”，然后将它添加到顶级菜单中
filemenu = tk.Menu(MenuBar, tearoff=False,bg="#000",fg="#FFF")
filemenu.add_command(label="打开", command=GetFile)
filemenu.add_command(label="保存", command=SaveFile)
filemenu.add_command(label="新建", command=NewFile)
filemenu.add_command(label="运行", command=runpy)
filemenu.add_separator()
filemenu.add_command(label="退出", command=root.quit)
MenuBar.add_cascade(label="文件", menu=filemenu)
 
# 创建另一个“编辑”下拉菜单，然后将它添加到顶级菜单中
EditMenu = tk.Menu(MenuBar, tearoff=False,bg="#000",fg="#FFF")
EditMenu.add_command(label="剪切", command=no)
EditMenu.add_command(label="拷贝", command=no)
EditMenu.add_command(label="粘贴", command=no)
MenuBar.add_cascade(label="编辑", menu=EditMenu)
 
# 创建另一个“设置”下拉菜单，然后将它添加到顶级菜单中
settingmenu = tk.Menu(MenuBar, tearoff=False,bg="#000",fg="#FFF")
settingmenu.add_command(label="参数设置", command=CSSetWind)
settingmenu.add_command(label="文件设置", command=FileSetWind)
settingmenu.add_command(label="IDE设置", command=IDESetWind)
MenuBar.add_cascade(label="设置", menu=settingmenu)

# 创建另一个“帮助”下拉菜单，然后将它添加到顶级菜单中
helptmenu = tk.Menu(MenuBar,tearoff=False,bg="#000",fg="#FFF")
helptmenu.add_command(label="关于我们", command=no)
helptmenu.add_command(label="获取帮助", command=no)
helptmenu.add_command(label="软件信息", command=EXEInfo)
helptmenu.add_command(label="插件", command=Plugin)
MenuBar.add_cascade(label="帮助", menu=helptmenu)

menu = tk.Menu(root,bg="#000",fg="#FFF",tearoff=False)
menu.add_cascade(label = '复制',command=no)
menu.add_cascade(label = '粘贴',command=no)
menu.add_cascade(label = '运行',command=runpy)
showPopoutMenu(root, menu)

# 显示菜单
root.config(menu=MenuBar)

#窗口设置
root.iconphoto(True,tk.PhotoImage(file="image/cobweb.png"))
root.bind('<F9>',runpy)
root.geometry("600x450+374+182")
root.title("清云IDE")
root.mainloop()
