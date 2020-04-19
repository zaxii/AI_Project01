import sys
import numpy as np
import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow
from maze_ui import Ui_MainWindow

from QLearning import *
from Markov import *
from genMaze import gen_maze


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.reset()
        self.resetBtn.clicked.connect(self.reset)
        self.startBtn.clicked.connect(self.move)
        self.iterationBtn.clicked.connect(self.learn)
        self.Mode.clicked.connect(self.change_mode)
        self.unit = 50
        self.x = -1
        self.y = -1
        self.iteration_times = 0
        self.cur_mode = 1      # -1 Markov 1 Q

    def change_mode(self):
        self.cur_mode *= -1
        self.iteration_times = 0
        if self.cur_mode == -1:
            self.Mode.setText("Markov")
        else:
            self.Mode.setText("Qlearning")
        self.reset()

    def reset(self):
        gen_maze()
        with open('input.txt', 'r') as f:
            text = f.read()
            self.cur_maze = json.loads(text)
        self.Q_input = create_Qtable(self.cur_maze)
        self.M_table = create_Mtable(self.cur_maze)
        self.flush()
        self.iteration_times = 0
        self.iterationMsg.setText("N = " + str(self.iteration_times))

    def learn(self):
        if self.cur_mode == 1:
            self.learn_Q()
        else:
            self.learn_M()

    def learn_Q(self):
        np.set_printoptions(precision=3, suppress=True)
        for t in range(5):
            self.Q_input = iteration_Q(self.cur_maze, self.Q_input)
        self.iteration_times += 5
        self.iterationMsg.setText("N = " + str(self.iteration_times))

    def learn_M(self):
        for t in range(5):
            self.M_table = iteration_M(self.cur_maze, self.M_table)
        self.iteration_times += 5
        self.iterationMsg.setText("N = " + str(self.iteration_times))

    def move(self):
        if self.Mode == -1:
            self.move_M()
        else:
            self.move_Q()

    def move_Q(self):
        pix = self.maze_window.pixmap()
        painter = QPainter(pix)
        Q_table = self.Q_input
        for i in range(10):
            for j in range(10):
                tmp = self.cur_maze[i][j]
                if tmp == 1:
                    painter.setBrush(QBrush(Qt.red))
                    painter.drawRect(self.unit * i, self.unit * j, 50, 50)
                elif tmp == -1:
                    painter.setBrush(QBrush(Qt.black))
                    painter.drawRect(self.unit * i, self.unit * j, 50, 50)
                elif tmp == -2:
                    painter.setBrush(QBrush(Qt.gray))
                    painter.drawRect(self.unit * i, self.unit * j, 50, 50)
        self.maze_window.repaint()
        step = 0
        max_step = 100
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

            cur_x, cur_y, flag = transfer(self.cur_maze, x, y, cur_x, cur_y)

            painter.setBrush(QBrush(Qt.white))
            painter.drawRect(x * self.unit, y * self.unit, 50, 50)

            painter.setBrush(QBrush(Qt.red))
            painter.drawRect((cur_x + 0.25) * self.unit, (cur_y + 0.25) * self.unit, 25, 25)
            self.maze_window.repaint()
            time.sleep(0.05)

            if flag:
                print("SUCCESS!!!!!!!!!!!!!!!!!!!!")
                break

            step += 1
            self.step.setText(str(step))
            if step >= max_step:
                painter.setBrush(QBrush(Qt.white))
                painter.drawRect(cur_x * self.unit, cur_y * self.unit, 50, 50)

    def move_M(self):
        pix = self.maze_window.pixmap()
        painter = QPainter(pix)
        value_record = self.M_table
        for i in range(10):
            for j in range(10):
                tmp = self.cur_maze[i][j]
                if tmp == 1:
                    painter.setBrush(QBrush(Qt.red))
                    painter.drawRect(self.unit * i, self.unit * j, 50, 50)
                elif tmp == -1:
                    painter.setBrush(QBrush(Qt.black))
                    painter.drawRect(self.unit * i, self.unit * j, 50, 50)
                elif tmp == -2:
                    painter.setBrush(QBrush(Qt.gray))
                    painter.drawRect(self.unit * i, self.unit * j, 50, 50)
        self.maze_window.repaint()

        cur_x, cur_y = 0, 0
        total_record = self.cur_maze + value_record
        step = 0
        max_step = 500
        while True:
            x = cur_x
            y = cur_y
            choice = choose_direction_M(total_record, cur_x, cur_y)
            cur_x, cur_y, flag = move(self.cur_maze, cur_x, cur_y, choice)
            painter.setBrush(QBrush(Qt.white))
            painter.drawRect(x * self.unit, y * self.unit, 50, 50)

            painter.setBrush(QBrush(Qt.red))
            painter.drawRect((cur_x + 0.25) * self.unit, (cur_y + 0.25) * self.unit, 25, 25)
            self.maze_window.repaint()
            time.sleep(0.05)
            if flag:
                break
            step += 1
            if step >= max_step:
                painter.setBrush(QBrush(Qt.white))
                painter.drawRect(cur_x * self.unit, cur_y * self.unit, 50, 50)

    def flush(self):
        canvas = QPixmap(500, 500)
        canvas.fill(Qt.white)
        self.maze_window.setPixmap(canvas)
        painter = QPainter(self.maze_window.pixmap())
        painter.setPen(QPen(Qt.black))
        unit = 50
        x = 0
        while x <= 500:
            painter.drawLine(x, 0, x, 500)
            x += unit
        y = 0
        while y <= 500:
            painter.drawLine(0, y, 500, y)
            y += unit


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())