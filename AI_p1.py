import numpy as np

gamma = 0.9
my_maze = [[0, 0, 0, 0],
           [0, -1, 0, 0],
           [0, 0, 0, 0],
           [0, 0, -1, 0],
           [0, 0, 0, 1]]


def iteration(cur_maze, value_record):
    new_value_record = np.zeros((len(cur_maze), len(cur_maze[0])))
    x_size, y_size = len(cur_maze), len(cur_maze[0])
    for x in range(x_size):
        for y in range(y_size):
            # 如果在地图上是障碍、陷阱或者终点，那么跳过
            if abs(cur_maze[x][y]) == 1:
                continue
            new_value_record[x][y] = Bellman(value_record, cur_maze, x, y)
    return new_value_record


def Bellman(value_record, cur_maze, x, y):
    x_size, y_size = len(cur_maze), len(cur_maze[0])
    value = -100
    # up
    if x == 0:
        cur_value = -1
    elif y == 0:  # 最小大于2*2
        cur_value = -0.2 + 0.6 * (cur_maze[x - 1][y] + gamma * value_record[x - 1][y]) \
                    + 0.2 * (cur_maze[x - 1][y + 1] + gamma * value_record[x - 1][y + 1])
    elif y == y_size - 1:
        cur_value = -0.2 + 0.6 * (cur_maze[x - 1][y] + gamma * value_record[x - 1][y]) \
                    + 0.2 * (cur_maze[x - 1][y - 1] + gamma * value_record[x - 1][y - 1])
    else:
        cur_value = 0.2 * (cur_maze[x - 1][y - 1] + gamma * value_record[x - 1][y - 1]) + \
                    0.6 * (cur_maze[x - 1][y] + gamma * value_record[x - 1][y]) \
                    + 0.2 * (cur_maze[x - 1][y + 1] + gamma * value_record[x - 1][y + 1])
    value = max(cur_value, value)

    # down
    if x == x_size - 1:
        cur_value = -1
    elif y == 0:
        cur_value = -0.2 + 0.6 * (cur_maze[x + 1][y] + gamma * value_record[x + 1][y]) \
                    + 0.2 * (cur_maze[x + 1][y + 1] + gamma * value_record[x + 1][y + 1])
    elif y == y_size - 1:
        cur_value = -0.2 + 0.6 * (cur_maze[x + 1][y] + gamma * value_record[x + 1][y]) \
                    + 0.2 * (cur_maze[x + 1][y - 1] + gamma * value_record[x + 1][y - 1])
    else:
        cur_value = 0.2 * (cur_maze[x + 1][y - 1] + gamma * value_record[x + 1][y - 1]) + \
                    0.6 * (cur_maze[x + 1][y] + gamma * value_record[x + 1][y]) \
                    + 0.2 * (cur_maze[x + 1][y + 1] + gamma * value_record[x + 1][y + 1])
    value = max(cur_value, value)

    # left
    if y == 0:
        cur_value = -1
    elif x == 0:
        cur_value = -0.2 + 0.6 * (cur_maze[x][y - 1] + gamma * value_record[x][y - 1]) \
                    + 0.2 * (cur_maze[x + 1][y - 1] + gamma * value_record[x + 1][y - 1])
    elif x == x_size - 1:
        cur_value = -0.2 + 0.6 * (cur_maze[x][y - 1] + gamma * value_record[x][y - 1]) \
                    + 0.2 * (cur_maze[x - 1][y - 1] + gamma * value_record[x - 1][y - 1])
    else:
        cur_value = 0.2 * (cur_maze[x + 1][y - 1] + gamma * value_record[x + 1][y - 1]) \
                    + 0.6 * (cur_maze[x][y - 1] + gamma * value_record[x][y - 1]) \
                    + 0.2 * (cur_maze[x - 1][y - 1] + gamma * value_record[x - 1][y - 1])
    value = max(cur_value, value)

    # right
    if y == y_size - 1:
        cur_value = -1
    elif x == 0:
        cur_value = -0.2 + 0.6 * (cur_maze[x][y + 1] + gamma * value_record[x][y + 1]) \
                    + 0.2 * (cur_maze[x + 1][y + 1] + gamma * value_record[x + 1][y + 1])
    elif x == x_size - 1:
        cur_value = -0.2 + 0.6 * (cur_maze[x][y + 1] + gamma * value_record[x][y + 1]) \
                    + 0.2 * (cur_maze[x - 1][y + 1] + gamma * value_record[x - 1][y + 1])
    else:
        cur_value = 0.2 * (cur_maze[x + 1][y + 1] + gamma * value_record[x + 1][y + 1]) \
                    + 0.6 * (cur_maze[x][y + 1] + gamma * value_record[x][y + 1]) \
                    + 0.2 * (cur_maze[x - 1][y + 1] + gamma * value_record[x - 1][y + 1])
    value = max(cur_value, value)
    return value


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


array = np.zeros((len(my_maze), len(my_maze[0])))
for i in range(5):
    array = iteration(my_maze, array)
    print(array)
