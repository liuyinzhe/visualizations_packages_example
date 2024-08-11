import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde

import marsilea as ma


# Create datasets

np.random.seed(0)
rs = np.random.RandomState(50)
x, y = rs.normal(size=(2, 50))
xmin, ymin, xmax, ymax = x.min(), y.min(), x.max(), y.max()

# 用于生成 一维二维和更高维度的整形网格
# 二维:np.mgrid[起始值:结束值:步长, 起始值:结束值:步长]
X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
positions = np.vstack([X.ravel(), Y.ravel()])
values = np.vstack([x, y])

# 核密度评估
# gaussian_kde 使用高斯核表示 kernel-density 估计
main_kernel = gaussian_kde(values)

Z = np.reshape(main_kernel(positions), X.shape)

x_kernel = gaussian_kde(x)
zx = x_kernel(np.mgrid[xmin:xmax:100j])

y_kernel = gaussian_kde(x)
# 长度
zy = y_kernel(np.mgrid[ymin:ymax:100j])


# Create skeletons and add contents

wb = ma.WhiteBoard(width=3, height=3)
# Reserve empty canvas for drawing latter
# add_canvas 添加一个新的子图到画布上,并且命名 ax
# Add an axes to the main canvas
wb.add_canvas("top", size=0.4, pad=0.1, name="x1")
wb.add_canvas("bottom", size=0.4, pad=0.1, name="x2")
wb.add_canvas("left", size=0.4, pad=0.1, name="y1")
wb.add_canvas("right", size=0.4, pad=0.1, name="y2")
# Add title
wb.add_title(left="Y-axis distribution", top="X-axis distribution")
# Add padding
wb.add_pad("left", size=0.3)
wb.add_pad("right", size=0.3)
# Initiate the axes
wb.render()

# sns 绘制在同一个画布上
# 获取主画布
main_ax = wb.get_main_ax()
# 配置关闭坐标刻度
main_ax.set_axis_off()
# matplotlib.axes.Axes.pcolormesh
# Create a pseudocolor plot with a non-regular rectangular grid.
# 使用非规则矩形网格创建伪彩色图
main_ax.pcolormesh(Z, cmap="Greens")

x1_ax = wb.get_ax("x1")
# 折线图：lineplot()
sns.lineplot(x=np.arange(len(zy)), y=zy, ax=x1_ax, color="b", alpha=0.7)
# 限制x轴长度
x1_ax.set_xlim(0, len(zy))
# 刻度关闭
x1_ax.tick_params(bottom=False, labelbottom=False)
# 边框控制 sns.despine 
# 删除上侧和右侧边缘线
sns.despine(ax=x1_ax)

x2_ax = wb.get_ax("x2")
x2_ax.set_axis_off()
# 底部蓝色密度条带
x2_ax.pcolormesh(zy.reshape(1, -1), cmap="Blues")

y1_ax = wb.get_ax("y1")
# 折线图：lineplot()
sns.lineplot(y=np.arange(len(zx)), x=zx, ax=y1_ax, orient="y", color="r", alpha=0.7)
# 限制y轴长度
y1_ax.set_ylim(0, len(zx))
sns.despine(ax=y1_ax, left=True, right=False)
# 刻度关闭
y1_ax.tick_params(right=False, labelright=False)
# x 轴刻度标签设置角度
for tick in y1_ax.get_xticklabels():
    tick.set_rotation(90)
# x 轴翻转
y1_ax.invert_xaxis()

y2_ax = wb.get_ax("y2")
y2_ax.set_axis_off()
# 右侧红色密度条带
y2_ax.pcolormesh(zy.reshape(-1, 1), cmap="Reds")
# y 轴翻转
y2_ax.invert_yaxis()


plt.savefig("Bivariate_Distribution.png", bbox_inches="tight")
