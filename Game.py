import tkinter as tk
from tkinter import messagebox
from environment import *
from MCTS import *
import time


rate = 0.1  # 黑点占格子大小的百分比
rate_piece = 0.45  # 棋子占格子大小的百分比
grid = 40  # 每个格子的大小
color = (249, 214, 91)  # 棋盘颜色


class NoGoGame:
    def __init__(self):
        self.env = NoGoEnv()
        self.cur_color = 1
        self.env.reset()
        self.if_ai_action = False

        # 界面对象的基本参数设置
        self.root = tk.Tk()
        self.root.title("NoGo")
        # root.geometry('335x265+250+250')
        # 设置界面是否可以随意拉伸
        self.root.resizable(False, False)
        # 棋盘居中显示
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 10 * grid) / 2
        y = (screen_height - 10 * grid) / 2
        self.root.geometry("%dx%d+%d+%d" % (10 * grid, 10 * grid, x, y))

        self.canvas = tk.Canvas(self.root, bg='#F9D65B', height=grid * 10, width=grid * 10)
        self.canvas.grid(row=0, column=0)
        # 绘制线
        self.canvas.create_rectangle(grid / 2, grid / 2, 10 * grid - grid / 2, 10 * grid - grid / 2, width=2)
        for i in range(1, 10):
            self.canvas.create_line(grid, i * grid, 9 * grid, i * grid, fill='black')
            self.canvas.create_line(i * grid, grid, i * grid, 9 * grid, fill='black')
        # 绘制中心点
        self.canvas.create_oval(5 * grid - rate * grid, 5 * grid - rate * grid, 5 * grid + rate * grid,
                                5 * grid + rate * grid,
                                fill="black")

        # 鼠标事件
        self.canvas.bind("<Button-1>", lambda event: self.mouseEvent(event))
        self.AImaster()
        self.root.mainloop()

    def drawPiece(self, x, y):
        if self.cur_color == 1:
            self.canvas.create_oval(x * grid + rate_piece * grid, y * grid + rate_piece * grid, x * grid - rate_piece * grid,
                               y * grid - rate_piece * grid, fill="black")
        else:
            self.canvas.create_oval(x * grid + rate_piece * grid, y * grid + rate_piece * grid, x * grid - rate_piece * grid,
                               y * grid - rate_piece * grid, fill="white")

    def mouseEvent(self, event):
        if self.if_ai_action:
            return
        x = int(event.x + rate_piece * grid) // grid
        y = int(event.y + rate_piece * grid) // grid
        print(x, y)
        if x < 1 or x > 9 or y < 1 or y > 9:
            return
        self.step(x, y)
        self.AImaster()

    def step(self, x, y):
        self.drawPiece(x, y)
        _, reward, if_end = self.env.step(y - 1, x - 1)  # 注意这里的区别
        self.root.update() # 刷新
        self.cur_color = - self.cur_color
        if if_end:
            print(reward)
            self.GameEnd(reward)

    def gameReset(self):
        self.env.reset()
        self.canvas.delete("all")
        self.canvas = tk.Canvas(self.root, bg='#F9D65B', height=grid * 10, width=grid * 10)
        self.canvas.grid(row=0, column=0)
        self.canvas.create_rectangle(grid / 2, grid / 2, 10 * grid - grid / 2, 10 * grid - grid / 2, width=2)
        for i in range(1, 10):
            self.canvas.create_line(grid, i * grid, 9 * grid, i * grid, fill='black')
            self.canvas.create_line(i * grid, grid, i * grid, 9 * grid, fill='black')
        self.canvas.create_oval(5 * grid - rate * grid, 5 * grid - rate * grid, 5 * grid + rate * grid,
                                5 * grid + rate * grid,
                                fill="black")
        self.canvas.bind("<Button-1>", lambda event: self.mouseEvent(event))

    def AImaster(self):
        self.if_ai_action = True
        node = TreeNode(None, self.env.board, self.cur_color)
        choice = monte_carlo_tree_search(node)
        self.step(choice[1]+1, choice[0]+1)
        self.if_ai_action = False

    def GameEnd(self,reward):
        # 弹窗显示结果后刷新
        messagebox.showinfo(title='Game Over', message='Black Side Win' if reward['black_side']==10 else 'White Side Win')
        self.gameReset()


if __name__ == "__main__":
    game = NoGoGame()
'''
鼠标点击事件
<Button-1>  鼠标左键
<Button-2>   鼠标中间键（滚轮）
<Button-3>  鼠标右键
<Double-Button-1>   双击鼠标左键
<Double-Button-3>   双击鼠标右键
<Triple-Button-1>   三击鼠标左键
<Triple-Button-3>   三击鼠标右键
'''

