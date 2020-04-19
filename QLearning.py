import numpy as np
import json
import random
from utils import *
import matplotlib.pyplot as plt
from genMaze import gen_maze


def create_Qtable(cur_maze):
    x_size, y_size = len(cur_maze), len(cur_maze[0])
    q_table = np.zeros((x_size, y_size, 4))
    return q_table


def iteration_Q(cur_maze, Q_table):
    x_size, y_size = len(cur_maze), len(cur_maze[0])
    max_Q = np.max(Q_table, axis=2)
    new_Q = np.zeros((x_size, y_size, 4))

    for x in range(x_size):
        for y in range(y_size):
            # 跳过非路径块
            if not cur_maze[x][y] == 0:
                continue
            new_record = [0, 0, 0, 0]

            # up
            if x == 0:
                new_record[0] = wall_reward + gamma * max_Q[x][y]

            elif y == 0:  # 迷宫规格应当最小大于2*2
                new_record[0] = branch_probability * (wall_reward + gamma * max_Q[x][y])

                if cur_maze[x - 1][y] == wall_flag:
                    new_record[0] += main_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x - 1][y] == trap_flag:
                    new_record[0] += main_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[0] += main_probability * (cur_maze[x - 1][y] + gamma * max_Q[x - 1][y])

                if cur_maze[x - 1][y + 1] == wall_flag:
                    new_record[0] += branch_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x - 1][y + 1] == trap_flag:
                    new_record[0] += branch_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[0] += branch_probability * (cur_maze[x - 1][y + 1] + gamma * max_Q[x - 1][y + 1])

            elif y == y_size - 1:
                if cur_maze[x - 1][y - 1] == wall_flag:
                    new_record[0] += branch_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x - 1][y - 1] == trap_flag:
                    new_record[0] += branch_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[0] += branch_probability * (cur_maze[x - 1][y - 1] + gamma * max_Q[x - 1][y - 1])

                if cur_maze[x - 1][y] == wall_flag:
                    new_record[0] += main_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x - 1][y] == trap_flag:
                    new_record[0] += main_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[0] += main_probability * (cur_maze[x - 1][y] + gamma * max_Q[x - 1][y])

                new_record[0] += branch_probability * (wall_reward + gamma * max_Q[x][y])

            else:
                if cur_maze[x - 1][y - 1] == wall_flag:
                    new_record[0] += branch_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x - 1][y - 1] == trap_flag:
                    new_record[0] += branch_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[0] += branch_probability * (cur_maze[x - 1][y - 1] + gamma * max_Q[x - 1][y - 1])

                if cur_maze[x - 1][y] == wall_flag:
                    new_record[0] += main_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x - 1][y] == trap_flag:
                    new_record[0] += main_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[0] += main_probability * (cur_maze[x - 1][y] + gamma * max_Q[x - 1][y])

                if cur_maze[x - 1][y + 1] == wall_flag:
                    new_record[0] += branch_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x - 1][y + 1] == trap_flag:
                    new_record[0] += branch_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[0] += branch_probability * (cur_maze[x - 1][y + 1] + gamma * max_Q[x - 1][y + 1])

            # down
            if x == x_size - 1:
                new_record[1] = wall_reward + gamma * max_Q[x][y]

            elif y == 0:  # 迷宫规格应当最小大于2*2
                new_record[1] = branch_probability * (wall_reward + gamma * max_Q[x][y])

                if cur_maze[x + 1][y] == wall_flag:
                    new_record[1] += main_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x + 1][y] == trap_flag:
                    new_record[1] += main_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[1] += main_probability * (cur_maze[x + 1][y] + gamma * max_Q[x + 1][y])

                if cur_maze[x + 1][y + 1] == wall_flag:
                    new_record[1] += branch_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x + 1][y + 1] == trap_flag:
                    new_record[1] += branch_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[1] += branch_probability * (cur_maze[x + 1][y + 1] + gamma * max_Q[x + 1][y + 1])

            elif y == y_size - 1:
                if cur_maze[x + 1][y - 1] == wall_flag:
                    new_record[1] += branch_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x + 1][y - 1] == trap_flag:
                    new_record[1] += branch_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[1] += branch_probability * (cur_maze[x + 1][y - 1] + gamma * max_Q[x + 1][y - 1])

                if cur_maze[x + 1][y] == wall_flag:
                    new_record[1] += main_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x + 1][y] == trap_flag:
                    new_record[1] += main_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[1] += main_probability * (cur_maze[x + 1][y] + gamma * max_Q[x + 1][y])

                new_record[1] += branch_probability * (wall_reward + gamma * max_Q[x][y])

            else:
                if cur_maze[x + 1][y - 1] == wall_flag:
                    new_record[1] += branch_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x + 1][y - 1] == trap_flag:
                    new_record[1] += branch_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[1] += branch_probability * (cur_maze[x + 1][y - 1] + gamma * max_Q[x + 1][y - 1])

                if cur_maze[x + 1][y] == wall_flag:
                    new_record[1] += main_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x + 1][y] == trap_flag:
                    new_record[1] += main_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[1] += main_probability * (cur_maze[x + 1][y] + gamma * max_Q[x + 1][y])

                if cur_maze[x + 1][y + 1] == wall_flag:
                    new_record[1] += branch_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x - 1][y + 1] == trap_flag:
                    new_record[1] += branch_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[1] += branch_probability * (cur_maze[x + 1][y + 1] + gamma * max_Q[x + 1][y + 1])

            # left
            if y == 0:
                new_record[2] = wall_reward + gamma * max_Q[x][y]

            elif x == 0:  # 迷宫规格应当最小大于2*2
                new_record[2] = branch_probability * (wall_reward + gamma * max_Q[x][y])

                if cur_maze[x][y - 1] == wall_flag:
                    new_record[2] += main_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x][y - 1] == trap_flag:
                    new_record[2] += main_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[2] += main_probability * (cur_maze[x][y - 1] + gamma * max_Q[x][y - 1])

                if cur_maze[x + 1][y - 1] == wall_flag:
                    new_record[2] += branch_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x + 1][y - 1] == trap_flag:
                    new_record[2] += branch_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[2] += branch_probability * (cur_maze[x + 1][y - 1] + gamma * max_Q[x + 1][y - 1])

            elif x == x_size - 1:
                if cur_maze[x - 1][y - 1] == wall_flag:
                    new_record[2] += branch_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x - 1][y - 1] == trap_flag:
                    new_record[2] += branch_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[2] += branch_probability * (cur_maze[x - 1][y - 1] + gamma * max_Q[x - 1][y - 1])

                if cur_maze[x][y - 1] == wall_flag:
                    new_record[2] += main_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x][y - 1] == trap_flag:
                    new_record[2] += main_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[2] += main_probability * (cur_maze[x][y - 1] + gamma * max_Q[x][y - 1])

                new_record[2] += branch_probability * (wall_reward + gamma * max_Q[x][y])

            else:
                if cur_maze[x - 1][y - 1] == wall_flag:
                    new_record[2] += branch_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x - 1][y - 1] == trap_flag:
                    new_record[2] += branch_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[2] += branch_probability * (cur_maze[x - 1][y - 1] + gamma * max_Q[x - 1][y - 1])

                if cur_maze[x][y - 1] == wall_flag:
                    new_record[2] += main_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x][y - 1] == trap_flag:
                    new_record[2] += main_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[2] += main_probability * (cur_maze[x][y - 1] + gamma * max_Q[x][y - 1])

                if cur_maze[x + 1][y - 1] == wall_flag:
                    new_record[2] += branch_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x + 1][y - 1] == trap_flag:
                    new_record[2] += branch_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[2] += branch_probability * (cur_maze[x + 1][y - 1] + gamma * max_Q[x + 1][y - 1])

            # right
            if y == y_size - 1:
                new_record[3] = wall_reward + gamma * max_Q[x][y]

            elif x == 0:  # 迷宫规格应当最小大于2*2
                new_record[3] = branch_probability * (wall_reward + gamma * max_Q[x][y])

                if cur_maze[x][y + 1] == wall_flag:
                    new_record[3] += main_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x][y + 1] == trap_flag:
                    new_record[3] += main_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[3] += main_probability * (cur_maze[x][y + 1] + gamma * max_Q[x][y + 1])

                if cur_maze[x + 1][y + 1] == wall_flag:
                    new_record[3] += branch_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x + 1][y + 1] == trap_flag:
                    new_record[3] += branch_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[3] += branch_probability * (cur_maze[x + 1][y + 1] + gamma * max_Q[x + 1][y + 1])

            elif x == x_size - 1:
                if cur_maze[x - 1][y + 1] == wall_flag:
                    new_record[3] += branch_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x - 1][y + 1] == trap_flag:
                    new_record[3] += branch_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[3] += branch_probability * (cur_maze[x - 1][y + 1] + gamma * max_Q[x - 1][y + 1])

                if cur_maze[x][y + 1] == wall_flag:
                    new_record[3] += main_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x][y + 1] == trap_flag:
                    new_record[3] += main_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[3] += main_probability * (cur_maze[x][y + 1] + gamma * max_Q[x][y + 1])

                new_record[3] += branch_probability * (wall_reward + gamma * max_Q[x][y])

            else:
                if cur_maze[x - 1][y + 1] == wall_flag:
                    new_record[3] += branch_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x - 1][y + 1] == trap_flag:
                    new_record[3] += branch_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[3] += branch_probability * (cur_maze[x - 1][y + 1] + gamma * max_Q[x - 1][y + 1])

                if cur_maze[x][y + 1] == wall_flag:
                    new_record[3] += main_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x][y + 1] == trap_flag:
                    new_record[3] += main_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[3] += main_probability * (cur_maze[x][y + 1] + gamma * max_Q[x][y + 1])

                if cur_maze[x + 1][y + 1] == wall_flag:
                    new_record[3] += branch_probability * (wall_reward + gamma * max_Q[x][y])
                elif cur_maze[x + 1][y + 1] == trap_flag:
                    new_record[3] += branch_probability * (trap_reward + gamma * max_Q[0][0])
                else:
                    new_record[3] += branch_probability * (cur_maze[x + 1][y + 1] + gamma * max_Q[x + 1][y + 1])

            for k in range(4):
                new_Q[x][y][k] = (1 - alpha) * Q_table[x][y][k] + alpha * new_record[k]
    file = open("Q_table.txt", 'w')
    file.write(json.dumps(new_Q))
    return new_Q


def find_way_Q(cur_maze, Q_table):
    step = 0
    max_step = 50000
    cur_x, cur_y = 0, 0
    while step < max_step:
        direction = choose_direction_Q(Q_table[cur_x][cur_y])
        tmp = random.random()
        if tmp < 0.6:
            offset = 0
        elif tmp < 0.8:
            offset = -1
        else:
            offset = 1

        x = cur_x
        y = cur_y

        if direction == 0:
            cur_x += -1
            cur_y += offset

        elif direction == 1:
            cur_x += 1
            cur_y += offset

        elif direction == 2:
            cur_x += offset
            cur_y += -1

        else:
            cur_x += offset
            cur_y += 1
        # print("当前落点: ", cur_x, cur_y)
        cur_x, cur_y, flag = transfer(cur_maze, x, y, cur_x, cur_y)
        if flag:
            # print(str(step), "SUCCESS!!!!!!!!!!!!!!!!!!!!")
            return step
        step += 1


def transfer(cur_maze, x, y, cur_x, cur_y):
    x_size, y_size = len(cur_maze), len(cur_maze[0])
    if (cur_x < 0 or cur_x >= x_size) or (cur_y < 0 or cur_y >= y_size) or cur_maze[cur_x][cur_y] == wall_flag:
        return x, y, False
    if cur_maze[cur_x][cur_y] == trap_flag:
        return 0, 0, False
    if cur_maze[cur_x][cur_y] == final_flag:
        return cur_x, cur_y, True
    return cur_x, cur_y, False


def choose_direction_Q(Q_direction):
    max_queue = [0]
    max_value = Q_direction[0]
    d = 1
    while d < 4:
        if Q_direction[d] > max_value:
            max_queue.clear()
            max_queue.append(d)
            max_value = Q_direction[d]
        elif Q_direction[d] == max_value:
            max_queue.append(d)
        d += 1
    ran = random.randint(0, len(max_queue) - 1)
    policy = max_queue[ran]  # 贪心策略
    is_greedy = random.random() < epsilon
    if not is_greedy:
        tmp = [0, 1, 2, 3]
        tmp.pop(policy)
        policy = tmp[random.randint(0, 2)]
    return policy


def a_test():
    gen_maze()
    with open('input.txt', 'r') as f:
        text = f.read()
        my_maze = json.loads(text)
    Q_input = create_Qtable(my_maze)
    np.set_printoptions(precision=3, suppress=True)
    x_axis = range(50)
    y_axis = []
    for i in range(50):
        Q_input = iteration_Q(my_maze, Q_input)
        n = 0
        for k in range(10):
            n += find_way_Q(my_maze, Q_input)
        y_axis.append(n/10)

    plt.plot(x_axis, y_axis)
    for xp, yp in zip(x_axis, y_axis):
        if yp < 20:
            plt.text(xp, yp, yp, ha='center', va='bottom', fontsize=10)
    plt.show()


if __name__ == "__main__":
    a_test()
