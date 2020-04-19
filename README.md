# AI_Project01

**生成地图：**

python genMaze.py x y

其中x, y为可选参数，分别为地图障碍数与地图陷阱数，默认分别为5与3，上限为40，40，地图大小固定为10x10。

------

**Sarsa与Sarsa-Lambda运行说明：**

python Sarsarun.py –show

-show为可选参数，添加即可视化训练过程。

不添加则只显示地图形状。

运行结束之后会保存折线图至./Sarsa.jpg

--------

python SarsaLambdarun.py –show

-show为可选参数，添加即可视化训练过程。

不添加则只显示地图形状。

运行结束之后会保存折线图至./SarsaLambda.jpg

--------

**Markov、Qlearning与ui运行说明：**

python Markov.py

直接运行文件会生成一个随机地图并进行五十次迭代，每次迭代会将找到终点的步数的平均值生成一张折线图。

--------

python Qlearning.py

直接运行文件会生成一个随机地图并进行五十次迭代，每次迭代会将找到终点的步数的平均值生成一张折线图。

python ui.py

点击Markov(Qlearning)切换算法，reset重新生成地图，start开始寻路， N 显示迭代次数。为了可视化的需要，每一步会存在一定的时间间隔，因此设置了一个最大步数，防止时间过长。





**即时回报参数:**

边界外：-1

障碍：-0.5

终点：1

陷阱：-1

通路：0

**Qlearning,马尔可夫,Sarsa与Sarsa-Lambda参数：**

learning-rate: 0.1

greedy: 0.99

reward_decay: 1

lambda: 0.9

 
