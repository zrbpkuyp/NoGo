def in_board(x, y):
    return 0 <= x < 9 and 0 <= y < 9


cx = [-1, 0, 1, 0]
cy = [0, -1, 0, 1]


class NoGoEnv:

    def __init__(self):
        self.board = [[0 for col in range(9)] for row in range(9)]
        self.dfs_air_visit = [[0 for col in range(9)] for row in range(9)]
        self.curr_bot_color = 1  # 1 black -1 white
        self.black_piece_count = 0
        self.white_piece_count = 0
        self.history = []
        self.if_end = False
        self.winner = 0

    def reset(self):
        self.board = [[0 for col in range(9)] for row in range(9)]
        self.dfs_air_visit = [[0 for col in range(9)] for row in range(9)]
        self.curr_bot_color = 1
        self.black_piece_count = 0
        self.white_piece_count = 0
        self.history = []
        self.if_end = False
        self.winner = 0

    def step(self, x, y):
        if not self.proc_step(x, y, self.curr_bot_color):
            self.if_end = True
            self.winner = -self.curr_bot_color
        self.history.append([x, y])
        if self.check_has_valid_move(-self.curr_bot_color):
            self.if_end = True
            self.winner = self.curr_bot_color
        self.curr_bot_color = -self.curr_bot_color
        return self._obs(), self._reward(), self.if_end

    def dfs_air(self, fx, fy):
        self.dfs_air_visit[fx][fy] = True  # 为了防止搜索重复，标记走过的路
        flag = False
        for dir in range(4):
            dx = fx + cx[dir]
            dy = fy + cy[dir]
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
        for dir in range(4):  # 看旁边的棋子有没有气
            dx = fx + cx[dir]
            dy = fy + cy[dir]
            if in_board(dx, dy):
                if self.board[dx][dy] and not self.dfs_air_visit[dx][dy]:
                    if not self.dfs_air(dx, dy):
                        self.board[fx][fy] = 0
                        return False
        self.board[fx][fy] = 0
        return True

    def check_has_valid_move(self, col):  # true means game end
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and self.judge_available(i, j, col):
                    return False
        return True

    def proc_step(self, x, y, color, check_only=False):
        if not in_board(x, y) or self.board[x][y]:  # 出界或者被下过
            return False
        if not self.judge_available(x, y, color):  # 判断是否合法
            return False
        if not check_only:
            self.board[x][y] = color
        return True

    def _reward(self):
        if not self.if_end:
            return {"black_side": 0, "white_side": 0}
        if self.winner == 1:
            return {"black_side": 10, "white_side": -10}
        else:
            return {"black_side": -10, "white_side": 10}

    def _obs(self):
        return {"board": self.board, "history": self.history}

