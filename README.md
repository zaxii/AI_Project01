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

-------

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

 
