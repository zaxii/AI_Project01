from math import floor

import numpy as np
import pandas as pd
import os
import time

from element import Element as e
from point import Point as pt


class SARSAMaze:
    def __init__(self, path=""):
        self.gamma = 0.9  # discount

        self.epsilon = 0.9  # greedy policy

        self.fresh_time = 0.3

        self.max_episode = 100

        self.learningrate = 0.01

        self.percent_move_accurate = 0.6
        self.percent_move_not_accurate = 0.2

        self.action = ['up', 'down', 'left', 'right']

        # TODO: read from file to get self.maze
        #
        # TODO: transform maze to reward
        #
        self.maze = [[e.PASS, e.PASS, e.PASS, e.PASS],
                     [e.PASS, e.BLOCK, e.PASS, e.PASS],
                     [e.PASS, e.PASS, e.PASS, e.PASS],
                     [e.PASS, e.PASS, e.TRAP, e.PASS],
                     [e.PASS, e.PASS, e.PASS, e.TERMINAL]]

        self.reward = [[0, 0, 0, 0],
                       [0, -1, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, -1, 0],
                       [0, 0, 0, 1]]

        self.x_size = len(self.maze)
        self.y_size = len(self.maze[0])
        self.initial_x = 0
        self.initial_y = 0
        self.terminal_x = 3
        self.terminal_y = 3

        self.n_states = self.x_size * self.y_size

        self.qtable = pd.DataFrame(columns=self.action, dtype=np.float64)

    def choose_action(self, observation):
        self.check_state(observation)
        rnd = np.random.uniform()

        # choose the best action:
        if rnd < self.epsilon:
            state_action = self.qtable.loc[observation, :]

            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        # randomly explore
        else:
            action = np.random.choice(self.action)
        return action

    def check_state(self, state):
        if state not in self.qtable.index:
            self.qtable = self.qtable.append(
                pd.Series(
                    [0]*len(self.action),
                    index = self.qtable.columns,
                    name = state,
                )
            )

    def sarsa(self, state, act, r, state_, act_):
        self.check_state(state_)
        qpredict = self.qtable.loc[state, act]
        if state_ != 'terminal':
            qtarget = r + self.gamma * self.qtable.loc[state_, act_]
        else:
            qtarget = r
        self.qtable.loc[state, act] += self.learningrate * (qtarget - qpredict)

    def act(self, observation, action):
        nowpt = pt(floor(observation / self.y_size), observation - self.y_size * floor(observation / self.y_size))


    def rl(self):
        for episode in range(100):

            observation = 0

            action = self.choose_action(observation)

            while True:

                observation_, reward, done = self.act(observation, action)