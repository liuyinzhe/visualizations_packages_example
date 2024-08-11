#Annotate stacked bar
# https://marsilea.readthedocs.io/en/stable/examples/Basics/plot_stacked_bar.html#annotate-stacked-bar

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import marsilea as ma
import marsilea.plotter as mp

# 锁定随机种子
np.random.seed(0)
data = np.random.randint(1, 100, (5, 10))
data = pd.DataFrame(data=data, index=list("abcde"))
'''
print(data)
    0   1   2   3   4   5   6   7   8   9
a  45  48  65  68  68  10  84  22  37  88
b  71  89  89  13  59  66  40  88  47  89
c  82  38  26  78  73  10  21  81  70  80
d  48  65  83  89  50  30  20  20  15  40
e  33  66  10  58  33  32  75  24  36  76
'''

'''
计算每一列的全部数值sum
# pandas.DataFrame.sum(axis=0)
print(data.sum(axis=0))
print(data.sum())
0    279
1    306
2    273
3    306
4    283
5    148
6    240
7    235
8    205
9    373
dtype: int64
'''
# 百分比绘制 堆叠图
bar = mp.StackBar(data / data.sum(), width=0.9, legend_kws=dict(title="Stacked Bar"))
# 分类条带
top_colors = mp.Colors([1, 1, 2, 2, 4], cmap="Set2", label="Category")
# 总数对应颜色热图
top_mesh = mp.ColorMesh(
    data.sum(), cmap="cool", label="Total", cbar_kws=dict(orientation="horizontal")
)

# 白板
wb = ma.WhiteBoard(width=3, height=3, margin=0.2)
# 添加图层
wb.add_layer(bar)
# 顶部添加颜色条带
wb.add_top(top_colors, size=0.2) # legend=False 可以隐藏 legend
# 顶部添加颜色热图条带
wb.add_top(top_mesh, size=0.2, pad=0.1)
wb.add_legends()
# 设置间隔
wb.set_margin(0.2)
# 最终渲染
wb.render()
# 保存图片
wb.save("Annotate_stacked_bar.png")


# 对于 marsilea 与 seaborn/matplotlib 的组合绘图
# 以及 marsilea.WhiteBoard 基础上的绘图使用 matplotlib.pyplot.savefig() 保存图片
# plt.savefig("Annotate_Stacked_Bar.png", bbox_inches="tight")
