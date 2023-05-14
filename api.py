import os
import tkinter as tk
import webbrowser

class alert:
    __mode = ""

    def __init__(self,data = "") -> str:
        self.data = data
        return None
    
    def GetPlugin(self) -> str:
        # folder path
        dir_path = r'plugin/'
        # list to store files
        res = []
        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                res.append(path)
        return res
    
    def alert(self) -> bool:
        try:
            answer = tk.messagebox.askokcancel(self.data)
            if answer:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        
    def ResCommmand(self,type = ""):
        try:
            file = open("config/command.json","w+")
            if type == "":
                print("Specify the command type")
                return True
            elif type == "parameter":
                file.close()
                return True
            elif type == "not":
                file.close()
                return True
            else:
                print("[ERROR404]")
                return False
        except Exception as e:
            print(e)
            return False
