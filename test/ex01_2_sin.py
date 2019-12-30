# coding: utf-8
#16K0021 佐藤翼
#課題[1](2)

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
#キャンバス上での50ピクセルが座標上での１に等しい
scale_x=100
scale_y=100

def plot(x,y):
    draw_point(scale_x*x+OX,OY-scale_y*y)

def f(x):
    return math.sin(x)*math.cos(10*x)

make_axes(OX,OY,1000,800)
start=0
end=4*math.pi
delta=0.001
x=start
while x<4*math.pi:
    plot(x,f(x))
    x=x+delta
