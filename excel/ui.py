import os,sys
import tkinter as tk
from valid import *
from gini2_1 import gini_cal

if getattr(sys, 'frozen', False):
    # frozen
    mdir = os.path.dirname(sys.executable)
else:
    # unfrozen
    mdir = os.path.dirname(os.path.realpath(__file__))
# mdir=os.path.dirname(__file__)
window=tk.Tk()
window.title('主席大人的基尼系数计算小工具 author by 青梅煮酒')
window.geometry('600x800')

canvas=tk.Canvas(window,height=200,width=400)
image_file=tk.PhotoImage(file=os.path.join(mdir,'huba3.gif'))
image=canvas.create_image(60,0,anchor='nw',image=image_file)
canvas.pack(side='top')

tk.Label(window,text='Pi').place(x=50,y=210)
# vcm=(window.register(onValidate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
pi=tk.Entry(window)
pi.place(x=160,y=210)
tk.Label(window,text='分组数:').place(x=50,y=250)
gi=tk.Entry(window)
gi.place(x=160,y=250)
tk.Label(window,text='excel文件路径:').place(x=50,y=290)
fi=tk.Entry(window)
fi.place(x=160,y=290)

def cal():
    out.delete('0.0',tk.END)
    flag,res=gini_cal(pi.get(),gi.get(),fi.get())
    if flag:
        out.insert('0.0','\n'.join(res))
    else:
        out.insert('0.0',res)
button=tk.Button(window,text='计算',width=15,height=2,command=cal).place(x=100,y=330)
tk.Label(window,text='结果').place(x=0,y=370)
out=tk.Text(window)
out.place(x=0,y=400)
# out.insert('0.0','111')


# l = tk.Label(window, 
#     text='OMG! this is TK!',    # 标签的文字
#     bg='green',     # 背景颜色
#     font=('Arial', 12),     # 字体和字体大小
#     width=15, height=2  # 标签长宽
#     )
# l.pack()

# b = tk.Button(window, 
#     text='hit me',      # 显示在按钮上的文字
#     width=15, height=2, 
#     command=hit_me)     # 点击按钮式执行的命令

# 输入框,任何输入内容显示为*
# e = tk.Entry(window,show='*')
# 文本框
# t = tk.Text(window,height=2)

window.mainloop()