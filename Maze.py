import numpy as np
import time
import sys
import tkinter as tk
from element import Element as e
import json

UNIT = 40  # pixels


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()

        self.percent_move_accurate = 0.6
        self.percent_move_not_accurate = 0.2

        self.action_space = ['up', 'right', 'down', 'left']
        self.n_actions = len(self.action_space)
        self.title('maze')
        # self.maze = [[e.PASS, e.PASS, e.PASS, e.PASS],
        #             [e.PASS, e.BLOCK, e.PASS, e.PASS],
        #             [e.PASS, e.PASS, e.PASS, e.PASS],
        #             [e.PASS, e.PASS, e.TRAP, e.PASS],
        #             [e.PASS, e.PASS, e.PASS, e.TERMINAL]]

        self._build_maze()
        self.geometry('{0}x{1}'.format(self.x_size * UNIT, self.x_size * UNIT))
        self.findterminal()

    def findterminal(self):
        for x in range(self.x_size):
            for y in range(self.y_size):
                if self.maze[x][y] == e.TERMINAL:
                    self.terminal_x, self.terminal_y = x, y

    def _build_maze(self):

        with open('input.txt', 'r') as f:
            self.maze = json.load(f)

        self.x_size = len(self.maze)
        self.y_size = len(self.maze[0])
        self.initial_x = 0
        self.initial_y = 0

        x = self.x_size
        y = self.y_size
        self.canvas = tk.Canvas(self, bg="white", height=x * UNIT, width=y * UNIT)

        for c in range(0, self.y_size * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, self.x_size * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, self.x_size * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, self.y_size * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        origin = np.array([20, 20])
        self.blocks = []
        self.traps = []
        # TODO: rewrite this part to judge trap and block

        for x in range(self.x_size):
            for y in range(self.y_size):
                if self.maze[x][y] == -1:
                    block_center = origin + np.array([UNIT * y, UNIT * x])
                    block = self.canvas.create_rectangle(
                        block_center[0] - 15, block_center[1] - 15,
                        block_center[0] + 15, block_center[1] + 15,
                        fill='black'
                    )
                    self.blocks.append(self.canvas.coords(block))
                if self.maze[x][y] == -2:
                    trap_center = origin + np.array([UNIT * y, UNIT * x])
                    trap = self.canvas.create_rectangle(
                        trap_center[0] - 15, trap_center[1] - 15,
                        trap_center[0] + 15, trap_center[1] + 15,
                        fill='grey'
                    )
                    self.traps.append(self.canvas.coords(trap))
                if self.maze[x][y] == 1:
                    oval_center = origin + np.array([UNIT * y, UNIT * x])
                    self.oval = self.canvas.create_oval(
                        oval_center[0] - 15, oval_center[1] - 15,
                        oval_center[0] + 15, oval_center[1] + 15,
                        fill='yellow')

        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')

        self.canvas.pack()

    def reset(self):
        self.update()
        # time.sleep(0.5)
        self.canvas.delete(self.rect)
        origin = np.array([20, 20])
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        # return observation
        return self.canvas.coords(self.rect)

    def step(self, action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        rnd = np.random.uniform()
        if action == 0:
            if rnd > self.percent_move_not_accurate * 2:
                base_action[1] -= UNIT
            elif rnd > self.percent_move_not_accurate:
                base_action[0] -= UNIT
                base_action[1] -= UNIT
            else:
                base_action[0] += UNIT
                base_action[1] -= UNIT
        elif action == 1:
            if rnd > self.percent_move_not_accurate * 2:
                base_action[0] += UNIT
            elif rnd > self.percent_move_not_accurate:
                base_action[0] += UNIT
                base_action[1] -= UNIT
            else:
                base_action[0] += UNIT
                base_action[1] += UNIT
        elif action == 2:
            if rnd > self.percent_move_not_accurate + self.percent_move_not_accurate:
                base_action[1] += UNIT
            elif rnd > self.percent_move_not_accurate:
                base_action[0] -= UNIT
                base_action[1] += UNIT
            else:
                base_action[0] += UNIT
                base_action[1] += UNIT
        elif action == 3:
            if rnd > self.percent_move_not_accurate + self.percent_move_not_accurate:
                base_action[0] -= UNIT
            elif rnd > self.percent_move_not_accurate:
                base_action[0] -= UNIT
                base_action[1] -= UNIT
            else:
                base_action[0] -= UNIT
                base_action[1] += UNIT
        reward = 0
        if s[0] + base_action[0] <= 0 or s[0] + base_action[0] >= self.y_size * UNIT:
            reward = -1
            base_action[0] = 0
            base_action[1] = 0
        elif s[1] + base_action[1] <= 0 or s[1] + base_action[1] >= self.x_size * UNIT:
            reward = -1
            base_action[0] = 0
            base_action[1] = 0

        self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent

        s_ = self.canvas.coords(self.rect)  # next state
        ret_action = np.array([0, 0])
        ret_action[0] = s_[0] - 5
        ret_action[1] = s_[1] - 5

        if reward == -1:
            return s_, reward, False

        # reward function
        if s_ == self.canvas.coords(self.oval):
            reward = 1
            done = True
            s_ = 'terminal'
        elif s_ in self.blocks:
            reward = -0.5
            done = False
            self.canvas.move(self.rect, -base_action[0], -base_action[1])
            s_ = self.canvas.coords(self.rect)
        elif s_ in self.traps:
            reward = -1
            done = False
            self.canvas.move(self.rect, -ret_action[0], -ret_action[1])
            s_ = self.canvas.coords(self.rect)
        else:
            reward = 0
            done = False

        return s_, reward, done

    def render(self):
        time.sleep(0.1)
        self.update()
