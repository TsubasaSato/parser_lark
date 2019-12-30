# -*- utf-8 -*-
# 16K0021 佐藤翼
# 課題集　問題１
from tkinter import *

tk = Tk()
canvas = Canvas(tk, width=500, height=400)
canvas.pack()


class Rect:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.right = width + left
        self.bottom = height + top

    def print(self):
        print("Rect:(%d,%d),(%d,%d)\n" % (self.left, self.top, self.right, self.bottom))

    def render(self):
        canvas.create_rectangle(self.left, self.top, self.right, self.bottom)


class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def print(self):
        print("The Center is (%d,%d) , Radius is %d ." % (self.x, self.y, self.r))

    def render(self):
        canvas.create_oval(
            self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r
        )


class Container:  # add,renderAll,リスト（コンテナ）
    def __init__(self):
        self.contents = []  # コンテナの用意

    def add(self, obj):
        self.contents.append(obj)

    def renderALL(self):
        for obj in self.contents:
            obj.render()  # ポリモーフィズム


cont = Container()
cont.add(Rect(100, 100, 100, 50))
cont.add(Circle(75, 100, 50))
cont.add(Rect(200, 200, 75, 75))
cont.renderALL()
