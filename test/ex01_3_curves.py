# coding: utf-8
#16K0021 佐藤翼
#課題[1](3)

from tkinter import *
import math

tk=Tk()

canvas=Canvas(tk,width=1000,height=800,bd=0)
canvas.pack()

def draw_point(x,y,r=1,c="black"):
    canvas.create_oval(x-r,y-r,x+r,y+r,fill=c,outline=c)

def make_axes(ox,oy,width,height):
    canvas.create_line(0,oy,width,oy)
    canvas.create_line(ox,0,ox,height)

#原点
OX=300
OY=400
#キャンバス上での30ピクセルが座標上での１に等しい
scale_x=100
scale_y=100

def plot(x,y,c="black"):
    draw_point(scale_x*x+OX,OY-scale_y*y,c=c)

def f(y):
    return y*y
#aには角度の値が入る
def daen_x(a):
    return math.cos(a*math.pi)/4
def daen_y(a):
    return math.sin(a*math.pi)*2

make_axes(OX,OY,1000,800)
start=-2.0
srad=0
end=2.0
delta=0.001
a=srad
y=start
while a<2*end :
    plot(f(y),y,c="blue")
    plot(daen_x(a),daen_y(a),c="red")
    a=a+delta
    y=y+delta




