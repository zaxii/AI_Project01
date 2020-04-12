import numpy as np
from element import Element as E


class AIMazeFindPath:
    def __init__(self, path="", depth=10):
        self.gamma = 1
        self.reward_override = 0

        self.percent_move_accurate = 0.6
        self.percent_move_not_accurate = 0.2

        # TODO: read from file to get self.maze
        #
        # TODO: transform maze to reward
        #
        self.maze = [[E.PASS, E.PASS, E.PASS, E.PASS],
                     [E.PASS, E.BLOCK, E.PASS, E.PASS],
                     [E.PASS, E.PASS, E.PASS, E.PASS],
                     [E.PASS, E.PASS, E.TRAP, E.PASS],
                     [E.PASS, E.PASS, E.PASS, E.TERMINAL]]

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

        # TODO: gain the number of iterations.
        self.depth = depth
        self.value = np.zeros((self.depth + 1, self.x_size, self.y_size))
        self.result = np.zeros((self.depth + 1, self.x_size, self.y_size))

        # deal with N = 1
        self.result[1] = self.reward

    def iteration(self, now_depth):
        for x in range(self.x_size):
            for y in range(self.y_size):
                if abs(self.reward[x][y]) == 1:
                    continue
                self.value[now_depth + 1][x][y] = self.bellman(now_depth, x, y)
        self.result[now_depth + 1] = self.value[now_depth + 1] + self.reward

    def bellman(self, now_depth, x, y):
        record_value = -100

        # action: move up
        if x == 0:
            sigma_leftup = self.percent_move_not_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])
            sigma_up = self.percent_move_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])
            sigma_rightup = self.percent_move_not_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])
        else:
            if self.maze[x - 1][y] == E.BLOCK:
                value_next = self.value[now_depth][x][y]
            elif self.maze[x - 1][y] == E.TRAP:
                value_next = self.value[now_depth][self.initial_x][self.initial_y]
            else:
                value_next = self.value[now_depth][x - 1][y]
            sigma_up = self.percent_move_accurate * (self.reward[x - 1][y] + self.gamma * value_next)

            if y == 0:
                sigma_leftup = self.percent_move_not_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])

                if self.maze[x - 1][y + 1] == E.BLOCK:
                    value_next = self.value[now_depth][x][y]
                elif self.maze[x - 1][y + 1] == E.TRAP:
                    value_next = self.value[now_depth][self.initial_x][self.initial_y]
                else:
                    value_next = self.value[now_depth][x - 1][y + 1]
                sigma_rightup = self.percent_move_not_accurate * (self.reward[x - 1][y + 1] + self.gamma * value_next)
            elif y + 1 == self.y_size:
                if self.maze[x - 1][y - 1] == E.BLOCK:
                    value_next = self.value[now_depth][x][y]
                elif self.maze[x - 1][y - 1] == E.TRAP:
                    value_next = self.value[now_depth][self.initial_x][self.initial_y]
                else:
                    value_next = self.value[now_depth][x - 1][y - 1]
                sigma_leftup = self.percent_move_not_accurate * (self.reward[x - 1][y - 1] + self.gamma * value_next)

                sigma_rightup = self.percent_move_not_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])
            else:
                if self.maze[x - 1][y - 1] == E.BLOCK:
                    value_next = self.value[now_depth][x][y]
                elif self.maze[x - 1][y - 1] == E.TRAP:
                    value_next = self.value[now_depth][self.initial_x][self.initial_y]
                else:
                    value_next = self.value[now_depth][x - 1][y - 1]
                sigma_leftup = self.percent_move_not_accurate * (self.reward[x - 1][y - 1] + self.gamma * value_next)

                if self.maze[x - 1][y + 1] == E.BLOCK:
                    value_next = self.value[now_depth][x][y]
                elif self.maze[x - 1][y + 1] == E.TRAP:
                    value_next = self.value[now_depth][self.initial_x][self.initial_y]
                else:
                    value_next = self.value[now_depth][x - 1][y + 1]
                sigma_rightup = self.percent_move_not_accurate * (self.reward[x - 1][y + 1] + self.gamma * value_next)
        action_value = sigma_leftup + sigma_up + sigma_rightup
        record_value = max(record_value, action_value)

        # action: move down
        if x + 1 == self.x_size:
            sigma_leftdown = self.percent_move_not_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])
            sigma_down = self.percent_move_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])
            sigma_rightdown = self.percent_move_not_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])
        else:
            if self.maze[x + 1][y] == E.BLOCK:
                value_next = self.value[now_depth][x][y]
            elif self.maze[x + 1][y] == E.TRAP:
                value_next = self.value[now_depth][self.initial_x][self.initial_y]
            else:
                value_next = self.value[now_depth][x + 1][y]
            sigma_down = self.percent_move_accurate * (self.reward[x + 1][y] + self.gamma * value_next)

            if y == 0:
                sigma_leftdown = self.percent_move_not_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])

                if self.maze[x + 1][y + 1] == E.BLOCK:
                    value_next = self.value[now_depth][x][y]
                elif self.maze[x + 1][y + 1] == E.TRAP:
                    value_next = self.value[now_depth][self.initial_x][self.initial_y]
                else:
                    value_next = self.value[now_depth][x + 1][y + 1]
                sigma_rightdown = self.percent_move_not_accurate * (self.reward[x + 1][y + 1] + self.gamma * value_next)
            elif y + 1 == self.y_size:
                if self.maze[x + 1][y - 1] == E.BLOCK:
                    value_next = self.value[now_depth][x][y]
                elif self.maze[x + 1][y - 1] == E.TRAP:
                    value_next = self.value[now_depth][self.initial_x][self.initial_y]
                else:
                    value_next = self.value[now_depth][x + 1][y - 1]
                sigma_leftdown = self.percent_move_not_accurate * (self.reward[x + 1][y - 1] + self.gamma * value_next)

                sigma_rightdown = self.percent_move_not_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])
            else:
                if self.maze[x + 1][y - 1] == E.BLOCK:
                    value_next = self.value[now_depth][x][y]
                elif self.maze[x + 1][y - 1] == E.TRAP:
                    value_next = self.value[now_depth][self.initial_x][self.initial_y]
                else:
                    value_next = self.value[now_depth][x + 1][y - 1]
                sigma_leftdown = self.percent_move_not_accurate * (self.reward[x + 1][y - 1] + self.gamma * value_next)

                if self.maze[x + 1][y + 1] == E.BLOCK:
                    value_next = self.value[now_depth][x][y]
                elif self.maze[x + 1][y + 1] == E.TRAP:
                    value_next = self.value[now_depth][self.initial_x][self.initial_y]
                else:
                    value_next = self.value[now_depth][x + 1][y + 1]
                sigma_rightdown = self.percent_move_not_accurate * (self.reward[x + 1][y + 1] + self.gamma * value_next)
        action_value = sigma_leftdown + sigma_down + sigma_rightdown
        record_value = max(record_value, action_value)

        # action: move left
        if y == 0:
            sigma_leftup = self.percent_move_not_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])
            sigma_left = self.percent_move_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])
            sigma_leftdown = self.percent_move_not_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])
        else:
            if self.maze[x][y - 1] == E.BLOCK:
                value_next = self.value[now_depth][x][y]
            elif self.maze[x][y - 1] == E.TRAP:
                value_next = self.value[now_depth][self.initial_x][self.initial_y]
            else:
                value_next = self.value[now_depth][x][y - 1]
            sigma_left = self.percent_move_accurate * (self.reward[x][y - 1] + self.gamma * value_next)

            if x == 0:
                sigma_leftup = self.percent_move_not_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])

                if self.maze[x + 1][y - 1] == E.BLOCK:
                    value_next = self.value[now_depth][x][y]
                elif self.maze[x + 1][y - 1] == E.TRAP:
                    value_next = self.value[now_depth][self.initial_x][self.initial_y]
                else:
                    value_next = self.value[now_depth][x + 1][y - 1]
                sigma_leftdown = self.percent_move_not_accurate * (self.reward[x + 1][y - 1] + self.gamma * value_next)
            elif x + 1 == self.x_size:
                if self.maze[x - 1][y - 1] == E.BLOCK:
                    value_next = self.value[now_depth][x][y]
                elif self.maze[x - 1][y - 1] == E.TRAP:
                    value_next = self.value[now_depth][self.initial_x][self.initial_y]
                else:
                    value_next = self.value[now_depth][x - 1][y - 1]
                sigma_leftup = self.percent_move_not_accurate * (self.reward[x - 1][y - 1] + self.gamma * value_next)

                sigma_leftdown = self.percent_move_not_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])
            else:
                if self.maze[x - 1][y - 1] == E.BLOCK:
                    value_next = self.value[now_depth][x][y]
                elif self.maze[x - 1][y - 1] == E.TRAP:
                    value_next = self.value[now_depth][self.initial_x][self.initial_y]
                else:
                    value_next = self.value[now_depth][x - 1][y - 1]
                sigma_leftup = self.percent_move_not_accurate * (self.reward[x - 1][y - 1] + self.gamma * value_next)

                if self.maze[x + 1][y - 1] == E.BLOCK:
                    value_next = self.value[now_depth][x][y]
                elif self.maze[x + 1][y - 1] == E.TRAP:
                    value_next = self.value[now_depth][self.initial_x][self.initial_y]
                else:
                    value_next = self.value[now_depth][x + 1][y - 1]
                sigma_leftdown = self.percent_move_not_accurate * (self.reward[x + 1][y - 1] + self.gamma * value_next)
        action_value = sigma_leftup + sigma_left + sigma_leftdown
        record_value = max(record_value, action_value)

        # action: move right
        if y + 1 == self.y_size:
            sigma_rightup = self.percent_move_not_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])
            sigma_right = self.percent_move_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])
            sigma_rightdown = self.percent_move_not_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])
        else:
            if self.maze[x][y + 1] == E.BLOCK:
                value_next = self.value[now_depth][x][y]
            elif self.maze[x][y + 1] == E.TRAP:
                value_next = self.value[now_depth][self.initial_x][self.initial_y]
            else:
                value_next = self.value[now_depth][x][y + 1]
            sigma_right = self.percent_move_accurate * (self.reward[x][y + 1] + self.gamma * value_next)

            if x == 0:
                sigma_rightup = self.percent_move_not_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])

                if self.maze[x + 1][y + 1] == E.BLOCK:
                    value_next = self.value[now_depth][x][y]
                elif self.maze[x + 1][y + 1] == E.TRAP:
                    value_next = self.value[now_depth][self.initial_x][self.initial_y]
                else:
                    value_next = self.value[now_depth][x + 1][y + 1]
                sigma_rightdown = self.percent_move_not_accurate * (self.reward[x + 1][y + 1] + self.gamma * value_next)
            elif x + 1 == self.x_size:
                if self.maze[x - 1][y + 1] == E.BLOCK:
                    value_next = self.value[now_depth][x][y]
                elif self.maze[x - 1][y + 1] == E.TRAP:
                    value_next = self.value[now_depth][self.initial_x][self.initial_y]
                else:
                    value_next = self.value[now_depth][x - 1][y + 1]
                sigma_rightup = self.percent_move_not_accurate * (self.reward[x - 1][y + 1] + self.gamma * value_next)

                sigma_rightdown = self.percent_move_not_accurate * (self.reward_override + self.gamma * self.value[now_depth][x][y])
            else:
                if self.maze[x - 1][y + 1] == E.BLOCK:
                    value_next = self.value[now_depth][x][y]
                elif self.maze[x - 1][y + 1] == E.TRAP:
                    value_next = self.value[now_depth][self.initial_x][self.initial_y]
                else:
                    value_next = self.value[now_depth][x - 1][y + 1]
                sigma_rightup = self.percent_move_not_accurate * (self.reward[x - 1][y + 1] + self.gamma * value_next)

                if self.maze[x + 1][y + 1] == E.BLOCK:
                    value_next = self.value[now_depth][x][y]
                elif self.maze[x + 1][y + 1] == E.TRAP:
                    value_next = self.value[now_depth][self.initial_x][self.initial_y]
                else:
                    value_next = self.value[now_depth][x + 1][y + 1]
                sigma_rightdown = self.percent_move_not_accurate * (self.reward[x + 1][y + 1] + self.gamma * value_next)
        action_value = sigma_rightup + sigma_right + sigma_rightdown
        record_value = max(record_value, action_value)

        return record_value

    def run(self):
        # TODO: calculate time cost
        for now_depth in range(1, self.depth, 1):
            self.iteration(now_depth)

    def show_result(self):
        print(self.result)

    def show_value(self):
        print(self.value)


# def calculate_probability(x_size, y_size, x, y):
#     # 归一化
#     probability = [2, 3, 2, 3, 3, 2, 3, 2]
#     if y == 0:
#         probability[0] = probability[3] = probability[5] = 0
#     elif y == y_size - 1:
#         probability[2] = probability[4] = probability[7] = 0
#     if x == 0:
#         probability[0] = probability[1] = probability[2] = 0
#     elif x == x_size - 1:
#         probability[5] = probability[6] = probability[7] = 0
#     # tmp = sum(probability)
#     for i in range(len(probability)):
#         probability[i] /= 20
#     return probability

