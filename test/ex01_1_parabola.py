# coding: utf-8
#16K0021 佐藤翼
#課題[1](1)


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
OX=200
OY=400
#キャンバス上での30ピクセルが座標上での１に等しい
scale_x=30
scale_y=30

def plot(x,y):
    draw_point(scale_x*x+OX,OY-scale_y*y)

def f(y):
    return y*y

make_axes(OX,OY,1000,800)
start=-25.0
end=25.0
delta=0.001
y=start
while y<25.0:
    plot(f(y),y)
    y=y+delta




      
