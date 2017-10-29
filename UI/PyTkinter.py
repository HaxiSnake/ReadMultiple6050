#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tkinter控件初始化配置（默认为深色）
'''
__author__ = "jakey.chen"
__version__ = "v1.0"


import tkinter as tk

g_default_theme = "dark"
# g_default_theme = "default"

class PyButton(tk.Button):
    '''
    Button
    '''
    def __init__(self, master, theme=g_default_theme, **kv):
        self.theme = theme
        self.kv = kv
        self.temp = dict()
        self.choose_theme()
        tk.Button.__init__(self, master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "activebackground": "#00B2EE",
                                "activeforeground": "#E0EEEE",
                                "bg": "#008B8B",
                                "fg": "#FFFFFF"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

            for key,value in self.kv.items():
                self.temp[key] = value

class PyLabel(tk.Label):
    '''
    Label
    '''
    def __init__(self, master, theme=g_default_theme, **kv):
        self.theme = theme
        self.kv = kv
        self.temp = dict()
        self.choose_theme()
        tk.Label.__init__(self, master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929",
                                "fg": "#E0EEEE"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

            for key,value in self.kv.items():
                self.temp[key] = value

class PyLabelFrame(tk.LabelFrame):
    '''
    Frame
    '''
    def __init__(self, master, theme=g_default_theme, **kv):
        self.theme = theme
        self.kv = kv
        self.temp = dict()
        self.choose_theme()
        tk.LabelFrame.__init__(self, master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929",
                                "fg": "#1E90FF"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

            for key,value in self.kv.items():
                self.temp[key] = value

class PyListbox(tk.Listbox):
    '''
    Listbox
    '''
    def __init__(self, master, theme=g_default_theme, **kv):
        self.theme = theme
        self.kv = kv
        self.temp = dict()
        self.choose_theme()
        tk.Listbox.__init__(self, master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929",
                                "fg": "#1E90FF",
                                "selectbackground": "#00B2EE"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

            for key,value in self.kv.items():
                self.temp[key] = value

class PyText(tk.Text):
    '''
    Text
    '''
    def __init__(self, master, theme=g_default_theme, **kv):
        self.theme = theme
        self.kv = kv
        self.temp = dict()
        self.choose_theme()
        tk.Text.__init__(self, master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929",
                                "fg": "#1E90FF"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

            for key,value in self.kv.items():
                self.temp[key] = value

class PyCheckbutton(tk.Checkbutton):
    '''
    Checkbutton
    '''
    def __init__(self, master, theme=g_default_theme, **kv):
        self.theme = theme
        self.kv = kv
        self.temp = dict()
        self.choose_theme()
        tk.Checkbutton.__init__(self, master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929",
                                "fg": "#FFFFFF",
                                "activebackground": "#292929",
                                "activeforeground": "#FFFFFF",
                                "selectcolor": "#292929"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

            for key,value in self.kv.items():
                self.temp[key] = value

class PyRadiobutton(tk.Radiobutton):
    '''
    Radiobutton
    '''
    def __init__(self, master, theme=g_default_theme, **kv):
        self.theme = theme
        self.kv = kv
        self.temp = dict()
        self.choose_theme()
        tk.Radiobutton.__init__(self, master, self.temp) 

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929",
                                "fg": "#FFFFFF",
                                "activebackground": "#292929",
                                "selectcolor": "#292929"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

            for key,value in self.kv.items():
                self.temp[key] = value


class PyEntry(tk.Entry):
    '''
    Entry
    '''
    def __init__(self, master, theme=g_default_theme, **kv):
        self.theme = theme
        self.kv = kv
        self.temp = dict()
        self.choose_theme()
        tk.Entry.__init__(self, master, self.temp)

    def choose_theme(self):
        if self.theme == "dark":
            dark_theme_dict = {
                                "bg": "#292929",
                                "fg": "#E0EEEE",
                                "insertbackground": "#E0EEEE"
                              }
            for key,value in dark_theme_dict.items():
                self.temp[key] = value

            for key,value in self.kv.items():
                self.temp[key] = value

if __name__ == '__main__':
    root = tk.Tk()
    root.configure(bg="#292929")
    PyButton(root, text="1234", font=("Monaco", 12)).pack()
    PyLabel(root, text="label", font=("Monaco", 15)).pack()
    PyCheckbutton(root, text="123", font=("Monaco", 15)).pack()
    PyEntry(root, font=("Monaco", 15)).pack()
    PyText(root, font=("Monaco", 15), height=2, width=20).pack()
    listbox_0 = PyListbox(root, height=2, font=("Monaco", 15))
    listbox_0.pack()
    for i in range(2):
        listbox_0.insert("end", i)
    radio_intvar = tk.IntVar()
    PyRadiobutton(root, text="001", variable=radio_intvar, value=0, font=("Monaco", 15)).pack()
    PyRadiobutton(root, text="002", variable=radio_intvar, value=1, font=("Monaco", 15)).pack()
    radio_intvar.set(1)

    root.mainloop()