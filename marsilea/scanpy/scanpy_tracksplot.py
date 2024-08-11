import numpy as np
import scanpy as sc
import matplotlib.pyplot as plt

pbmc = sc.datasets.pbmc3k_processed().raw.to_adata()
'''
print(pbmc)

AnnData object with n_obs × n_vars = 2638 × 13714
    obs: 'n_genes', 'percent_mito', 'n_counts', 'louvain'
    var: 'n_cells'
    uns: 'draw_graph', 'louvain', 'louvain_colors', 'neighbors', 'pca', 'rank_genes_groups'
    obsm: 'X_pca', 'X_tsne', 'X_umap', 'X_draw_graph_fr'
    obsp: 'distances', 'connectivities'

'''


# Define the cells and markers that we want to draw

cell_markers = {
    "CD4 T cells": ["IL7R"],
    "CD14+ Monocytes": ["CD14", "LYZ"],
    "B cells": ["MS4A1"],
    "CD8 T cells": ["CD8A"],
    "NK cells": ["GNLY", "NKG7"],
    "FCGR3A+ Monocytes": ["FCGR3A", "MS4A7"],
    "Dendritic cells": ["FCER1A", "CST3"],
    "Megakaryocytes": ["PPBP"],
}

cells, markers = [], []
for c, ms in cell_markers.items():
    cells += [c] * len(ms)
    markers += ms

uni_cells = list(cell_markers.keys())
cell_colors = [
    "#568564",
    "#DC6B19",
    "#F72464",
    "#005585",
    "#9876DE",
    "#405559",
    "#58DADA",
    "#F85959",
]
cmapper = dict(zip(uni_cells, cell_colors))

# Draw
import marsilea as ma
import marsilea.plotter as mp

exp = pbmc[:, markers].X.toarray()
'''
marsilea.base.ZeroHeightCluster
A utility class to initialize a canvas with zero height and cluster data

Parameters:
cluster_data
    ndarray
    The cluster data

width
    float
    The width of the main canvas in inches

name
    str
    The name of the main canvas

margin
    float, 4-tuple
    The margin of the main canvas in inches
'''
#print(exp.T)
'''
[[1.3862944 1.0986123 0.6931472 ... 0.        0.        0.       ]
 [0.        0.        0.        ... 0.        0.        0.       ]
 [0.6931472 1.3862944 1.0986123 ... 0.        0.        0.6931472]
 ...
 [0.        0.        0.        ... 0.        0.        0.       ]
 [0.        0.6931472 0.6931472 ... 0.        0.        0.6931472]
 [0.        0.        0.        ... 0.        0.        0.       ]]
'''
# 堆叠图
tp = ma.ZeroHeightCluster(exp.T, width=20)
tp_anno = ma.ZeroHeight(width=1)
# 分组
tp.group_cols(pbmc.obs["louvain"], order=uni_cells, spacing=0.005)
# 顶部聚类
tp.add_dendrogram("top", add_base=False, size=1)

# 遍历每一个markers 绘制对应的折线图
for row, gene_name in zip(exp.T, markers):
    '''
    Area is a plotter for drawing area plot.
    区域折线图
    '''
    area = mp.Area(
        row,
        add_outline=False,
        alpha=1,
        group_kws={"color": cell_colors},
    )
    tp.add_bottom(area, size=0.4, pad=0.1)
# 底部添加颜色条带 # cmapper  颜色对应，自定义
tp.add_bottom(mp.Colors(pbmc.obs["louvain"], palette=cmapper), size=0.1, pad=0.1)
# 添加文字 ,fill_colors 参数被 mp.Colors 执行了，用于添加分组条带
tp.add_bottom(mp.Chunk(uni_cells, rotation=90))
# 一般这样 
# cell_colors 是颜色list 不能指定颜色
# m.add_top(mp.Chunk(uni_cells, fill_colors=cell_colors, rotation=90)) #字体大小fontsize :'small', 'medium', 'large',float

(tp + 0.1 + tp_anno).render()
plt.savefig("scanpy_tracksplot.png", bbox_inches="tight")

# plot_obj = tp + 0.1 + tp_anno
# plot_obj.render()
# plot_obj.save("scanpy_tracksplot.png")