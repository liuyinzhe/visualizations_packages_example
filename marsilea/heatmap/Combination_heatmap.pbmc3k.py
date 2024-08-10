# 引入marsilea
import marsilea as ma
import marsilea.plotter as mp
# 引入其他相关的包
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from sklearn.preprocessing import normalize

# 获取数据
pbmc3k = ma.load_data("pbmc3k")
#pbmc3k dict{'name':pandas.dataframe}
exp = pbmc3k["exp"]
pct_cells = pbmc3k["pct_cells"]
count = pbmc3k["count"]

# dataframe转为numpy 矩阵,按照行 进行归一化
matrix = normalize(exp.to_numpy(), axis=0)

cell_cat = ["Lymphoid", "Myeloid", "Lymphoid", "Lymphoid",
      "Lymphoid", "Myeloid", "Myeloid", "Myeloid"]
cell_names = ["CD4 T", "CD14\nMonocytes", "B", "CD8 T",
        "NK", "FCGR3A\nMonocytes", "Dendritic", "Megakaryocytes"]

# 创建可视化
# SizedMesh is a plotter that create a mesh plot with different sizes of markers.
# 添加不同大小圆圈
cells_proportion = mp.SizedMesh(
    pct_cells,
    size_norm=Normalize(vmin=0, vmax=100), # 大小 归一化
    color="none", # 填充颜色
    edgecolor="#6E75A4", # 边缘颜色
    linewidth=2, #线宽
    sizes=(1, 600), # 大小范围
    size_legend_kws=dict(title="% of cells", show_at=[0.3, 0.5, 0.8, 1]),
)

# MarkerMesh is a plotter that displays a 2D array as a mesh with markers.
# 添加星形标记
mark_high = mp.MarkerMesh(matrix > 0.7, color="#DB4D6D", label="High")

# Numbers is to display numbers in a bar plot.
# 展示数字柱状图
cell_count = mp.Numbers(count["Value"], color="#fac858", label="Cell Count")

# Violin is a wrapper for seaborn’s violinplot.
# 展示小提琴图
cell_exp = mp.Violin(exp, label="Expression", linewidth=0, color="#ee6666", density_norm="count")

# 添加标签
# Labels is to draw text labels on the plot.

cell_types = mp.Labels(cell_names, align="center")
gene_names = mp.Labels(exp.columns)

# Group plots together
h = ma.Heatmap(matrix, cmap="Greens", label="Normalized\nExpression", width=4.5, height=5.5)
# 添加图层
h.add_layer(cells_proportion) # 圆圈
h.add_layer(mark_high) # 星形

# 四周添加图
h.add_right(cell_count, pad=0.1, size=0.7) # cell_count 柱状图
h.add_top(cell_exp, pad=0.1, size=0.75, name="exp") # cell_exp 小提琴图
h.add_left(cell_types)  # cell_types 文字标签
h.add_bottom(gene_names) # gene_names 文字标签

# Grouping
# 根据 cell_cat 中两个类型,排序并分割为热图的两部分
'''
cell_cat = ["Lymphoid", "Myeloid", "Lymphoid", "Lymphoid",
      "Lymphoid", "Myeloid", "Myeloid", "Myeloid"]
'''
h.group_rows(group=cell_cat, order=["Lymphoid", "Myeloid"]) 
#h.hsplit(labels=cell_cat, order=["Lymphoid", "Myeloid"])
# 先分割hsplit,然后添加Chunk,分类标签(条形颜色)
h.add_left(mp.Chunk(["Lymphoid", "Myeloid"], ["#33A6B8", "#B481BB"]), pad=0.05)

# 添加聚类排序
h.add_dendrogram("left", colors=["#33A6B8", "#B481BB"])
h.add_dendrogram("bottom")

# 添加右侧图注
# align_legends 图例对齐基准 top
# align_stacks 图例堆积方式
# pad 间距
h.add_legends("right", align_stacks="center", align_legends="top", pad=0.2)

# 设置主画布的边距
# Set margin of the main canvas
# The margin of the main canvas in inches
h.set_margin(0.2)
# 最终渲染
h.render()

h.save("pkmc3k.png")
