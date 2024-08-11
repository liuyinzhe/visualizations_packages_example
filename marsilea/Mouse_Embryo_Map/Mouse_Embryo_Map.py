
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import pyplot as plt
from legendkit import cat_legend
import marsilea as ma

# Load dataset and prepare data

embryo = ma.load_data("mouse_embryo")

# 最大值
xmax = embryo["cell_x"].max()
ymax = embryo["cell_y"].max()
# 正负对称的起始终止
xstart, xend = -xmax * 0.05, xmax * 1.05
ystart, yend = -ymax * 0.05, ymax * 1.05

'''
np.linspace() 是 NumPy 库中的一个函数，
用于在指定的起始点和结束点之间生成等间隔的数值序列。
这个函数非常适用于需要精确控制元素间隔的场合。
'''
xrange = np.linspace(xstart, xend, 200)
yrange = np.linspace(ystart, yend, 200)

# 取中间值
xmid = (xrange[1:] + xrange[:-1]) / 2
ymid = (yrange[1:] + yrange[:-1]) / 2


def get_xy_hist(ct):
    '''
    获得xy坐标的直方图
    np.histogram 用于计算一维数组的直方图

    import numpy as np
    data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    hist, bins = np.histogram(data, bins=5)
    print("直方图统计结果：", hist)
    print("区间边界值：", bins)

    直方图统计结果： [2 2 2 2 2]
    区间边界值： [ 1.   2.8  4.6  6.4  8.2 10. ]
    '''
    x = embryo[embryo["cell_type"] == ct]["cell_x"].to_numpy()
    y = embryo[embryo["cell_type"] == ct]["cell_y"].to_numpy()
    xhist, _ = np.histogram(x, bins=xrange)
    yhist, _ = np.histogram(y, bins=yrange)
    return xhist, yhist

# Here we have a predefined colormap for each cell type.

colormap = {
    "Cavity": "#6d32e6",
    "Brain": "#bf024f",
    "Meninges": "#d147a3",
    "Choroid plexus": "#b3a726",
    "Cartilage primordium": "#103a14",
    "Jaw and tooth": "#ef833a",
    "Connective tissue": "#b38b5c",
    "Epidermis": "#35586d",
    "Lung primordium": "#3cb44b",
    "Sympathetic nerve": "#dfdce0",
    "Liver": "#bd3add",
    "Mucosal epithelium": "#0bd3b1",
    "GI tract": "#ff4374",
    "Mesentery": "#b74c11",
    "Dorsal root ganglion": "#036df4",
    "Muscle": "#dd7936",
    "Mesothelium": "#5c5ca6",
    "Blood vessel": "#be9b72",
    "Urogenital ridge": "#d3245a",
    "Heart": "#03fff4",
    "Pancreas": "#f062f9",
    "Kidney": "#62cfe8",
    "Ovary": "#c923b1",
}

width = 5
height = width * (yend - ystart) / (xend - xstart)
# 白板
b = ma.WhiteBoard(height=height, width=width)

# 根据细胞类型添加子图
cell_types = ["Brain", "Cartilage primordium", "Liver", "Heart", "GI tract"]
for n in cell_types:
    # 添加子图
    b.add_canvas("bottom", size=0.2, pad=0.1, name=f"{n}-x")
    b.add_canvas("right", size=0.2, pad=0.1, name=f"{n}-y")
b.render()

# Draw cell
ax = b.get_main_ax()
# matplotlib.axes.Axes.scatter() 散点图
points = ax.scatter(embryo["cell_x"], embryo["cell_y"], s=1, c=embryo["colors"])
# 强制栅格化（位图）绘制矢量图形输出
# matplotlib.artist.Artist.set_rasterized
# Force rasterized (bitmap) drawing for vector graphics output.
points.set_rasterized(True)
# 限制 x/y 轴范围
ax.set_xlim(xstart, xend)
ax.set_ylim(ystart, yend)
# 设置标题
ax.set_title("Mouse Embryo E12.5")
# 关闭x/y轴刻度
# matplotlib.axes.Axes.set_axis_off
# Hide all visual components of the x- and y-axis.
ax.set_axis_off()

# 分别取列表
colors = list(colormap.values())
labels = list(colormap.keys())

# 猜测是 指定 legend 颜色分配
# 具有相同手柄的分类图例
# 这对于创建共享的图例很有用 相同的手柄，但颜色不同
# Categorical legend with same handles
# This is useful to create legend that share the same handle but with different colors
cat_legend(colors=colors, labels=labels, ax=ax, loc="out left center", fontsize=10)

for n in cell_types:
    xh, yh = get_xy_hist(n)
    cmap = LinearSegmentedColormap.from_list(n, ["white", colormap[n]])
    x_ax = b.get_ax(f"{n}-x")
    # 密度过渡的条带图
    # 使用不规则矩形网格创建伪彩色图 
    # Create a pseudocolor plot with a non-regular rectangular grid.
    x_ax.pcolormesh(xh.reshape(1, -1), cmap=cmap)
    x_ax.set_axis_off()
    x_ax.text(0, 0.5, n, va="center", ha="right", transform=x_ax.transAxes)

    y_ax = b.get_ax(f"{n}-y")
    # 密度过渡的条带图
    # 使用不规则矩形网格创建伪彩色图 
    # Create a pseudocolor plot with a non-regular rectangular grid.
    y_ax.pcolormesh(yh.reshape(-1, 1), cmap=cmap)
    y_ax.set_axis_off()
    y_ax.text(0.5, 0, n, va="top", ha="center", rotation=90, transform=y_ax.transAxes)


# sphinx_gallery_ignore_start

# 对于 marsilea 与 seaborn/matplotlib 的组合绘图
# 以及 marsilea.WhiteBoard 基础上的绘图使用 matplotlib.pyplot.savefig() 保存图片
plt.savefig("Mouse_Embryo_Map.png", bbox_inches="tight")