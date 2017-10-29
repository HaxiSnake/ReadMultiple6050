import time
import logging
import threading
import platform

from UI import UITool
from SerialHelper import Read6050
from IOProcess.DataSave import *

import tkinter as tk 
from tkinter import ttk

logging.basicConfig(level=logging.DEBUG,\
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',\
                    datefmt='%a, %d %b %Y %H:%M:%S')
class MainSerialToolUI(UITool.SerialToolUI):
    def __init__(self,master = None):
        super(MainSerialToolUI,self).__init__()
        self.ser = None
        self.port_list = list()
        self.ser_list  = list()
        self.thread_read  = list()
        self.ser_all_alive = False
        self.thread_record = None
    def Open(self):
        '''
        打开关闭串口
        '''
        if self.frm_up_btn["text"] == "Open":
            try:
                ser_num = 0 #记录当前处理的com
                self.port_list = list()
                #得到端口号
                for index,item in enumerate(self.frm_up_setport_combobox):
                    ser_num = index
                    name = item.get()
                    if name == '-1' :
                        self.port_list.append("NONE")
                    else:
                        self.port_list.append("COM"+name)
                #print (self.port_list)
                #开启串口
                success_com =""
                self.ser_list = list()
                success_count = 0
                for index,port in enumerate(self.port_list):
                    ser_num = index
                    if port == "NONE":
                        #print ("NONE PORT")
                        continue
                    #print (type(port))
                    self.ser_list.append(Read6050(Port=port)) 
                    #print (type(self.ser_list[index])) 
                for index,ser in enumerate(self.ser_list):
                    ser_num = index
                    ser.open()
                    ser.setDaemon(True)
                    if ser.alive:
                        success_com = success_com + ser.port[3:] + " " 
                        success_count = success_count + 1 
                if success_count == len(self.ser_list):
                    self.ser_all_alive = True   
                    #print ("success com:",success_com)
                #开启读取线程
                if self.ser_all_alive is True:
                    self.frm_status_label["text"] = "[{0}] Opened!".format(success_com)
                    self.frm_status_label["fg"] = "#66CD00"
                    self.frm_up_btn["text"] = "Close"
                    self.frm_up_btn["bg"] = "#F08080"
                    for index,ser in enumerate(self.ser_list):
                        ser_num = index
                        ser.start()
            except Exception as e:
                logging.error(e)
                try:
                    self.frm_status_label["text"] = "Open [{0}] Failed!".format(self.ser_list[ser_num])
                    self.frm_status_label["fg"] = "#DC143C"
                except Exception as ex:
                    logging.error(ex)

        elif self.frm_up_btn["text"] == "Close":
            try:
                for ser in self.ser_list:
                    ser.stop()
                self.ser_all_alive = False
            except Exception as e:
                logging.error(e)
            self.frm_up_btn["text"] = "Open"
            self.frm_up_btn["bg"] = "#008B8B"
            self.frm_status_label["text"] = "Close Serial!"
            self.frm_status_label["fg"] = "#8DEEEE"
    def Record(self):
        '''记录和停止记录'''
        if self.frm_down_btn1["text"] == "Record":
            #print(self.frm_up_btn["text"],self.ser_all_alive)
            if self.frm_up_btn["text"] == "Close" and self.ser_all_alive:#串口打开状态
                self.thread_record = RecordThread(self.ser_list)
                self.thread_record.start()
                self.frm_status_label["text"] = "Recording Data..."
                self.frm_down_btn1["text"] = "Stop"
                self.frm_down_btn1["bg"] = "#F08080"
        elif self.frm_down_btn1["text"] == "Stop":
            self.thread_record.stop()
            self.frm_status_label["text"] = "Record Stopped"
            self.frm_down_btn1["text"] = "Record"
            self.frm_down_btn1["bg"] = "#008B8B"
if __name__ == '__main__':
    '''
    main loop
    '''
    root = tk.Tk()
    root.title("Serial Tool")
    if UITool.g_default_theme == "dark":
        root.configure(bg="#292929")
        combostyle = ttk.Style()
        combostyle.theme_use('alt')
        combostyle.configure("TCombobox", selectbackground="#292929", fieldbackground="#292929",\
                                          background="#292929", foreground="#FFFFFF")
    MainSerialToolUI(master=root)
    root.resizable(False, False)
    root.mainloop()