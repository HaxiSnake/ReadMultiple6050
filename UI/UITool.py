#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.getcwd())
import tkinter as tk
from tkinter import ttk
from UI import PyTkinter as pytk
from UI import Adaptive

font = Adaptive.monaco_font
size_dict = Adaptive.size_dict
g_default_theme = pytk.g_default_theme


class SerialToolUI(object):
    def __init__(self, master=None):
        self.root = master
        self.create_frame()
        self.thresholdValue = 1

    def create_frame(self):
        '''
        新建窗口，分为上下2个部分，下半部分为状态栏
        '''
        self.frm = pytk.PyLabelFrame(self.root)
        self.frm_status = pytk.PyLabelFrame(self.root)

        self.frm.grid(row=0, column=0, sticky="wesn")
        self.frm_status.grid(row=1, column=0, sticky="wesn")

        self.create_frm()
        self.create_frm_status()

    def create_frm(self):
        '''
        上半部分窗口分为上下2个部分
        '''
        self.frm_up = pytk.PyLabelFrame(self.frm)
        self.frm_down = pytk.PyLabelFrame(self.frm)

        self.frm_up.pack(side="top",fill="both",padx=5, pady=5)
        self.frm_down.pack(expand="yes",fill="both",padx=5, pady=5)
        #self.frm_up.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")
        #self.frm_down.grid(row=1, column=0, padx=5, pady=5, sticky="wesn")

        self.create_frm_up()
        self.create_frm_down()
    def create_frm_up(self):
        self.frm_up_label = pytk.PyLabel(self.frm_up,\
                                         text="Serial Ports",\
                                         font=font)
        self.frm_up_label.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")
        self.frm_up_setport = pytk.PyLabelFrame(self.frm_up)
        self.frm_up_setport.grid(row=1, column=0, padx=5, pady=5, sticky="wesn")
        self.frm_up_btn = pytk.PyButton(self.frm_up,text="Open",font=font,\
                                        command=self.Open)
        self.frm_up_btn.grid(row=2,column=0,padx=5,pady=5,sticky="wesn")
        self.create_frm_up_setport()
        
    def create_frm_down(self):
        self.frm_down_btn1 = pytk.PyButton(self.frm_down,text="Record",\
                                            font=font,command=self.Record)
        self.frm_down_btn1.pack(expand="yes",fill="both", padx=5, pady=5)
        #self.frm_down_btn1.grid(row=0, column=0, padx=5, pady=5, sticky="wesn",rowspan=2,columnspan=2)
    def create_frm_up_setport(self):
        port_name_list = ['  ###1:', '  ###2:', '  ###3:', '  ###4:']
        for index, item in enumerate(port_name_list):
            frm_up_label_temp = pytk.PyLabel(self.frm_up_setport,\
                                             text=item,\
                                             font=('Monaco', 10))
            frm_up_label_temp.grid(row=index + 1, column=0,\
                                   padx=1, pady=2, sticky="wesn")
        com_id = list(range(-1, 20, 1))
        self.frm_up_setport_combobox = []
        for i in range(4):
            self.frm_up_setport_combobox.append(ttk.Combobox(self.frm_up_setport,\
                                                          width=10,\
                                                          values=com_id))
        for index, item in enumerate(self.frm_up_setport_combobox):
            item.grid(row=index + 1, column=1,\
                      padx=1, pady=2, sticky="wesn")
            item.current(0)
    def Record(self):
        '''开始记录'''
        pass
    def Stop(self):
        '''停止记录'''
        pass
    def Open(self):
        '''打开关闭串口'''
        pass
    def create_frm_status(self):
        '''
        下半部分状态栏窗口
        '''
        self.frm_status_label = pytk.PyLabel(self.frm_status, 
                                             text="Ready",
                                             font=font)
        self.frm_status_label.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")

    def Toggle(self):
        pass




if __name__ == '__main__':
    '''
    main loop
    '''
    root = tk.Tk()
    if g_default_theme == "dark":
        root.configure(bg="#292929")
        combostyle = ttk.Style()
        combostyle.theme_use('alt')
        combostyle.configure("TCombobox", selectbackground="#292929", fieldbackground="#292929",
                                          background="#292929", foreground="#FFFFFF")
    root.title("Serial-Tool")
    SerialToolUI(master=root)
    root.resizable(False, False)
    root.mainloop()
