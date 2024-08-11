import numpy as np
import scanpy as sc

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

agg = sc.get.aggregate(pbmc[:, markers], by="louvain", func=["mean", "count_nonzero"])
agg.obs["cell_counts"] = pbmc.obs["louvain"].value_counts()

'''
print(agg)
AnnData object with n_obs × n_vars = 8 × 12
    obs: 'louvain', 'cell_counts'
    var: 'n_cells'
    layers: 'mean', 'count_nonzero'

'''
agg_exp = agg.layers["mean"]
agg_count = agg.layers["count_nonzero"]
agg_cell_counts = agg.obs["cell_counts"].to_numpy()
'''
print(agg_cell_counts)
[1144  480  342  316  154  150   37   15]
'''
h, w = agg_exp.shape

size = agg_count / agg_cell_counts[:, np.newaxis]
m = ma.SizedHeatmap(
    size=size,
    color=agg_exp,
    cluster_data=size,
    height=h / 3,
    width=w / 3,
    edgecolor="lightgray", # 边缘颜色
    cmap="Blues",
    size_legend_kws=dict(
        colors="#538bbf",
        title="Fraction of cells\nin groups (%)",
        labels=["20%", "40%", "60%", "80%", "100%"],
        show_at=[0.2, 0.4, 0.6, 0.8, 1.0],
    ),
    color_legend_kws=dict(title="Mean expression\nin group"),
)

m.add_top(mp.Labels(markers), pad=0.1) # 字体大小fontsize :'small', 'medium', 'large',float
m.add_top(mp.Chunk(uni_cells, fill_colors=cell_colors, rotation=90)) #字体大小fontsize :'small', 'medium', 'large',float
m.group_cols(cells, order=uni_cells)

m.add_right(mp.Labels(agg.obs["louvain"], align="center"), pad=0.1) #字体大小fontsize :'small', 'medium', 'large',float
m.add_left(
    mp.Numbers(agg_cell_counts, color="#EEB76B", label="Count"), size=0.5, pad=0.1  # mp.Numbers width float 控制柱子宽度
)
m.add_dendrogram("right", pad=0.1)
m.add_legends()
m.render()

m.save("scanpy_dotplot.png")