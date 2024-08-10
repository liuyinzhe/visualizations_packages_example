# 引入numpy和marsilea
import numpy as np
import marsilea as ma
import marsilea.plotter as mp
#from matplotlib  import plot as plt

# 创建一些随机数据
data = np.random.rand(20, 20)
cat = np.random.choice(["A", "B", "C"], 20)
# ['C' 'C' 'B' 'C' 'B' 'B' 'C' 'A' 'C' 'A' 'B' 'B' 'B' 'B' 'C' 'A' 'A' 'B' 'A' 'A']

print(cat)
# 初始化热图
h = ma.Heatmap(data, linewidth=1)

# 条带
# 在左边加入一个colors 条带；作为分组也可以
# 设置了占位的大小（size）为0.2
# 设置与相邻的图间隔（pad）为0.1
h.add_left(mp.Colors(cat), size=.2, pad=.1)

# 聚类
# 在左边和顶部添加层次聚类
h.add_dendrogram("left")
h.add_dendrogram("top")

# 行名标记
# 在右侧添加文字标记
h.add_right(mp.Labels(cat), pad=.1)

# 均值柱状图
# 在右侧继续添加一个柱状图
# 按照均值添加，data.mean(axis=0),整行计算均值
# 设置与相邻的图间隔（pad）为0.1
h.add_right(mp.Bar(data.mean(axis=0)), pad=.1)

# 最终渲染
h.render()


'''
How to Save to file
https://marsilea.readthedocs.io/en/stable/how_to/save/plot_save.html
h = ma.Heatmap(data, width=3, height=3)
h.save("plot.png")

You can also save the plot use the matplotlib.pyplot.savefig().

import matplotlib.pyplot as plt
h = ma.Heatmap(data, width=3, height=3)
h.render()
plt.savefig("plot.pdf", bbox_inches="tight")
'''
h.save("heatmap.png")
# h.save("heatmap.pdf")
