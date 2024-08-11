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

import pandas as pd
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

exp = pbmc[:, markers].X.toarray()
agg = sc.get.aggregate(pbmc[:, markers], by="louvain", func=["mean", "count_nonzero"])


agg_exp = agg.layers["mean"]

gene_data = []
cdata = []
for row, gene_name in zip(exp.T, markers[:5]):
    # Transform data to wide-format, marsilea only supports wide-format
    '''
    # 长表 转为 宽表
    import pandas as pd
    # 示例数据
    data = {
        'ID': [1, 1, 1, 2, 2, 2],
        'Variable': ['A', 'B', 'C', 'A', 'B', 'C'],
        'Value': [10, 20, 30, 40, 50, 60]
    }
    # 创建DataFrame
    df = pd.DataFrame(data)
    # 长表转宽表
    wide_df = df.pivot(index='ID', columns='Variable', values='Value')
    print(df)

        ID Variable  Value
    0   1        A     10
    1   1        B     20
    2   1        C     30
    3   2        A     40
    4   2        B     50
    5   2        C     60
    
    print(wide_df)

    Variable   A   B   C
    ID
    1         10  20  30
    2         40  50  60
    '''
    pdata = (
        pd.DataFrame({"exp": row, "cell_type": pbmc.obs["louvain"]})
        .reset_index(drop=True)
        .pivot(columns="cell_type", values="exp")
    )
    gene_data.append([gene_name, pdata])
    cdata.append(pdata.median())

# Create color mappable
# pandas dataframe 合并
cdata = pd.concat(cdata, axis=1).T
vmin, vmax = np.asarray(cdata).min(), np.asarray(cdata).max()
# ScalarMappable 标量 映射到颜色
sm = ScalarMappable(norm=Normalize(vmin=vmin, vmax=vmax), cmap="Blues")

sv = ma.ZeroHeightCluster(agg_exp.T, width=3)
sv_anno = ma.ZeroHeight(width=1)

for gene_name, pdata in gene_data:
    # Calculate the color to display
    # 颜色转换为RGB
    palette = sm.to_rgba(pdata.median()).tolist()
    sv.add_bottom(
        mp.Violin(
            pdata,
            inner=None,
            linecolor=".7",
            linewidth=0.5,
            density_norm="width",
            palette=palette, # 颜色
        ),
        size=0.5,
        pad=0.1,
        legend=False,
    )
    sv_anno.add_bottom(mp.Title(gene_name, align="left"), size=0.5, pad=0.1)

# 添加底部标签
sv.add_bottom(mp.Labels(cdata.columns))
# 添加聚类
sv.add_dendrogram("top")

# To fake a legend
'''
    颜色热图
    ColorMesh is a plotter that displays a 2D array as a colored mesh.
'''
sv.add_bottom(
    mp.ColorMesh(
        cdata,
        cmap="Blues", # 彩虹色 蓝色过渡色
        cbar_kws={"title": "Median expression\nin group", "orientation": "horizontal"},
    ),
    size=0,
)
# 图片合并排版
comp = sv + 0.1 + sv_anno
# 添加图例
comp.add_legends()
comp.render()

comp.save("scanpy_stacked_violin.png")