import numpy as np
import random
from math import *
import time
cx = [-1, 0, 1, 0]
cy = [0, -1, 0, 1]
cur_player = 1


def in_board(x, y):
    return 0 <= x < 9 and 0 <= y < 9


class TreeNode:
    """
    蒙特卡洛搜索树的节点类
    """

    def __init__(self, _parent, _board, _color):
        """ define basic variable and initialize """
        self.parent = _parent
        self.children = []
        self.board = _board
        self.valid_action = []
        self.children_cur_num = 0
        self.children_max_num = 0
        self.value = 0.0
        self.n = 0
        self.ucb = 0.0
        self.color = _color
        self.dfs_air_visit = [[0 for col in range(9)] for row in range(9)]
        self.get_valid_action()


    def dfs_air(self, fx, fy):
        self.dfs_air_visit[fx][fy] = True  # 为了防止搜索重复，标记走过的路
        flag = False
        for _dir in range(4):
            dx = fx + cx[_dir]
            dy = fy + cy[_dir]
            if in_board(dx, dy):
                if self.board[dx][dy] == 0:
                    flag = True
                if self.board[dx][dy] == self.board[fx][fy] and not self.dfs_air_visit[dx][dy]:
                    if self.dfs_air(dx, dy):
                        flag = True
        return flag

    def judge_available(self, fx, fy, col):
        self.board[fx][fy] = col  # 假设下在这里，看下完后的情况
        self.dfs_air_visit = [[0 for col in range(9)] for row in range(9)]
        if not self.dfs_air(fx, fy):  # 如果自己没气，不合法，复原
            self.board[fx][fy] = 0
            return False
        for _dir in range(4):  # 看旁边的棋子有没有气
            dx = fx + cx[_dir]
            dy = fy + cy[_dir]
            if in_board(dx, dy):
                if self.board[dx][dy] and not self.dfs_air_visit[dx][dy]:
                    if not self.dfs_air(dx, dy):
                        self.board[fx][fy] = 0
                        return False
        self.board[fx][fy] = 0
        return True

    def get_valid_action(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and self.judge_available(i, j, self.color):
                    self.valid_action.append([i, j])
                    self.children_max_num += 1
        if self.children_max_num != 0:
            random.shuffle(self.valid_action)


def best_child(node):  # 若子节点都扩展完了，求UCB值最大的子节点
    if node.children_max_num > node.children_cur_num:
        return node
    max_ucb = -5201314
    best_sub_node = None
    for sub_node in node.children:
        sub_node.ucb = sub_node.value / (sub_node.n) + sqrt(2.0 * log(node.n) / (sub_node.n))
        if sub_node.ucb > max_ucb:
            max_ucb = sub_node.ucb
            best_sub_node = sub_node
    return best_sub_node


def expand(node):
    if node.children_max_num == 0:
        return None
    else:
        new_board = [[0 for col in range(9)] for row in range(9)]
        for i in range(9):
            for j in range(9):
                new_board[i][j] = node.board[i][j]
        action = node.valid_action[node.children_cur_num]
        new_board[action[0]][action[1]] = node.color
        node.children_cur_num += 1
        new_node = TreeNode(node, new_board, -node.color)
        node.children.append(new_node)
    return new_node


def default_policy(node):
    if node.children_max_num == 0:
        return -1
    else:
        my_valid_cnt = node.children_max_num
        new_board = [[0 for col in range(9)] for row in range(9)]
        for i in range(9):
            for j in range(9):
                new_board[i][j] = node.board[i][j]
        r_node = TreeNode(None,new_board,-node.color)
        enemy_valid_cnt = r_node.children_max_num
        return tan(0.75*(my_valid_cnt-enemy_valid_cnt)/(my_valid_cnt+enemy_valid_cnt))


def backup(node, r):
    node.n += 1
    node.value += r
    if node.parent != None:
        backup(node.parent, -r)


def tree_policy(node):
    while node.children_max_num != 0:
        if node.children_cur_num == node.children_max_num:
            node = best_child(node)
        else:
            sub_node = expand(node)
            return sub_node
    return node


def monte_carlo_tree_search(node):
    st = time.time()
    search_times = 30000
    for i in range(search_times):
        expand_node = tree_policy(node)
        reward = default_policy(expand_node)
        backup(expand_node, -reward)
        if time.time() - st > 2.9:
            break
    max_n = -1
    best_choice = 0
    for i in range(node.children_cur_num):
        # print(node.children[i].n)
        if node.children[i].n > max_n:
            max_n = node.children[i].n
            best_choice = i
    # print(node.children[best_choice].n/node.n)
    return node.valid_action[best_choice]


# myboard = [[0 for col in range(9)] for row in range(9)]
# node = TreeNode(None, myboard, cur_player)
# print(monte_carlo_tree_search(node))
# print(node.value)
# print(node.n)
