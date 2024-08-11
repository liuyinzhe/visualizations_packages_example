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

exp = pbmc[:, markers].X.toarray()

m = ma.Heatmap(exp, cmap="viridis", height=4, width=3)
# 分组
'''
group_rows(group, order=None, spacing=0.01)
Group rows into chunks

Parameters
:
group
array-like
The group of each row

order
array-like, optional
The order of the unique groups

spacing
float, optional
The spacing between each split chunks, default is 0.01
'''
m.group_rows(pbmc.obs["louvain"], order=uni_cells,spacing=0.03)

# Add to the heatmap
m.add_left(
    mp.Colors(list(pbmc.obs["louvain"]), palette=cmapper),
    size=0.1,
    pad=0.1,
)

m.add_left(mp.Chunk(uni_cells, rotation=0, align="center"))

m.add_top(mp.Labels(markers), pad=0.1)

# 聚类
m.add_dendrogram("right", add_base=False)

# legends
m.add_legends()
# title
m.add_title("Expression Profile")

m.render()

m.save("scanpy_heatmap.png")