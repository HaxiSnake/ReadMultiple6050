from tkinter import *

def change():
    print(v.get())#取出变量v的值
root = Tk()
v = IntVar()

Radiobutton(root,text='one',variable=v,value=1,command=change).pack(anchor=W)
Radiobutton(root,text='two',variable=v,value=2,command=change).pack(anchor=W)
Radiobutton(root,text='three',variable=v,value=3,command=change).pack(anchor=W)

root.mainloop()