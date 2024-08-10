import matplotlib as mpl
from matplotlib.ticker import FuncFormatter


import marsilea as ma

dataset = ma.load_data("sc_multiomics")
# print(dataset["protein_exp_matrix"]) #颜色矩阵都是数字
# ticker 文字格式设置
fmt = FuncFormatter(lambda x, _: f"{x:.0%}")

# 谱系分类
#lineage = ["B Cells", "T Cells", "Mono/DC", "Plasma"]
lineage = ["B Lymphocytes","T Lymphocytes", "Monocytes/DCs", "Plasma"]
lineage_colors = ["#D83F31", "#EE9322", "#E9B824", "#219C90"]

# 分类信息 lineage 与颜色进行字典绑定
m = dict(zip(lineage, lineage_colors))
# 聚类矩阵
cluster_data = dataset["gene_exp_matrix"]
# 互作信息
interaction = dataset["interaction"]
# 谱系细胞
lineage_cells = dataset["lineage_cells"]
# print(dataset)
# print(set(lineage_cells))
'''
("B Lymphocytes","T Lymphocytes", "Monocytes/DCs", "Plasma")
'''
marker_names = dataset["marker_names"]
#print(marker_names)
'''
['CD2' 'CD4' 'CD5' 'CD7' 'CD14' 'CD19' 'CD38' 'CD44' 'CD47' 'CD52' 'CD69'
 'CD83' 'CD99' 'CLEC12A' 'CR1' 'CXCR4' 'FCGR2A' 'HLA-F' 'ICAM1' 'ICOS'
 'IL7R' 'ITGA2B' 'ITGA4' 'ITGAX' 'ITGB1' 'ITGB2' 'ITGB7' 'KLRD1']
'''
# 细胞计数
cells_count = dataset["cells_count"]
# 展示细胞
display_cells = dataset["display_cells"]
#print(display_cells)
'''
['ASDC' 'B Exhausted' 'B Immature' 'B Malignant' 'B Naive'
 'B Non-Switched Memory' 'B Switched Memory' 'C1$^+$ CD16$^+$ Mono.'
 'CD4$^+$ T$_{CM}$' 'CD4$^+$ T$_{EM}$' 'CD4$^+$ IL22' 'CD4$^+$ Naive'
 'CD4$^+$ T$_{fh}$' 'CD8$^+$ T$_{EM}$' 'CD8$^+$ Naive' 'CD8$^+$ T$_{E}$'
 'CD14$^+$ Mono.' 'CD16$^+$ Mono.' 'CD83$^+$ CD14$^+$ Mono.' 'MAIT'
 'Plasma cell IgA' 'Plasma cell IgG' 'Plasma cell IgM' 'Plasmablast'
 'Platelets' 'T Lymphocytes' 'T Lymphocytes' 'pDC']
'''

# matplotlib 设置文字大小
with mpl.rc_context({"font.size": 14}):
    # 热图 Sized Heatmap
    # Mesh for sized elements
    # 填充为mark,mark大小控制的热图
    # 基因热图
    gene_profile = ma.SizedHeatmap(
        dataset["gene_pct_matrix"],  # Control the radius of circles, must be numeric 控制mark圆半径,必须为数字
        color=dataset["gene_exp_matrix"], # 对应的颜色矩阵
        height=6,
        width=6,
        cluster_data=cluster_data,
        marker="P",  # mark
        cmap="PuRd", # 过渡颜色
        sizes=(1, 100), # 文件大小
        color_legend_kws={"title": "Mean Expression\n(RNA)"}, # 图例标题
        size_legend_kws={
            "colors": "#e252a4",
            "fmt": fmt, # 图例文字格式 fmt = FuncFormatter(lambda x, _: f"{x:.0%}")
            "title": "% expression in group", # 图例标题
        },
    )
    # 根据 lineage 排除拆分为多组
    #gene_profile.hsplit(labels=lineage_cells, order=lineage)
    gene_profile.group_rows(group=lineage_cells, order=lineage) 
    #先分割group_rows/hsplit组别,然后添加Chunk,分类标签(条形颜色)
    gene_profile.add_left(ma.plotter.Chunk(lineage, lineage_colors, padding=10))
    # 添加聚类
    gene_profile.add_dendrogram(
        "left",
        # scipy.cluster.hierarchy.linkage : method
        # method :single/complete/average/weighted/centroid/median/ward
        # single # Nearest Point Algorithm
        # complete # Farthest Point Algorithm or Voor Hees Algorithm
        # average # UPGMA algorithm
        # weighted # WPGMA
        # centroid # UPGMC algorithm
        # median # WPGMC algorithm
        # ward # Ward variance minimization algorithm. 
        method="ward",  
        colors=lineage_colors, # 指定聚类线条颜色
        meta_color="#451952", # 似乎这里没用
        linewidth=1.5,  # 线宽
    )
    # 底部添加文字标签
    gene_profile.add_bottom(
        ma.plotter.Labels(marker_names, color="#392467", align="bottom", padding=10)
    )

    # 按列剪切主画布
    #Cut the main canvas by columns
    #cut_cols(cut, spacing=0.01) 
    # cut # 用于指定剪切画布的位置的数据索引
    # spacing # 每次切割之间的间距，默认为 0.01
    # 切割为两份,方便后面add_bottom添加分组文字
    gene_profile.cut_cols([13])

    # 底部添加对组的 Mark groups
    # This is useful to mark each groups after you split the plot, the order of the chunks will align with cluster order.
    # 分割列排序将会对齐
    gene_profile.add_bottom(
        ma.plotter.Chunk(
            ["Cluster of Differentiation", "Other Immune"],
            ["#537188", "#CBB279"],
            padding=10,
        )
    )
    # 右侧添加文字标签
    gene_profile.add_right(
        ma.plotter.Labels(
            display_cells,
            text_props={"color": [m[c] for c in lineage_cells]},
            align="center",
            padding=10,
        )
    )
    # 添加标题
    gene_profile.add_title("Transcriptomics Profile", fontsize=16)

    # 蛋白热图
    protein_profile = ma.SizedHeatmap(
        dataset["protein_pct_matrix"], # Control the radius of circles, must be numeric 控制mark圆半径,必须为数字
        color=dataset["protein_exp_matrix"], # 对应的颜色矩阵
        cluster_data=cluster_data,
        marker="*",
        cmap="YlOrBr",
        height=6,
        width=6,
        color_legend_kws={"title": "Mean Expression\n(Protein)"}, # 单独对应颜色
        size_legend_kws={   # 单独对应大小的图注
            "colors": "#de600c",
            "fmt": fmt,
            "title": "% expression in group",
        },
    )
    # 分组
    #protein_profile.hsplit(labels=lineage_cells, order=lineage)
    protein_profile.group_rows(group=lineage_cells, order=lineage) 
    # 底部添加标签
    protein_profile.add_bottom(
        ma.plotter.Labels(marker_names, color="#E36414", align="bottom", padding=10)
    )
    # 左侧添加聚类,方法与gene_profile 一致，但是不显示聚类线条
    protein_profile.add_dendrogram("left", method="ward", show=False)

    # 基于互作打分在底部添加连线
    score = interaction["STRING Score"]
    '''interaction dataframe
            N1      N2  STRING Score    Type
    0     CD14  FCGR3A         0.430  Hetero
    1     CD14   ITGB2         0.736  Hetero
    2      CD2     CD4         0.403  Hetero
    3      CD2    IL7R         0.530  Hetero
    '''
    print(interaction[["N1", "N2"]].values)
    protein_profile.add_bottom(
        ma.plotter.Arc(
            marker_names, # 连线名字的列表
            interaction[["N1", "N2"]].values, # 名字之间的列表如[['CD14' 'FCGR3A'] ['CD14' 'ITGB2'] ['CD2' 'CD4']]
            # weights=score,
            colors=interaction["Type"].map({"Homo": "#864AF9", "Hetero": "#FF9BD2"}),
            labels=interaction["Type"], # type 标签
            width=1,
            legend_kws={"title": "PPI Type"}, # 图注标题
        ),
        size=2,
    )
    # 右侧添加数字柱状图
    # Show numbers in bar plot
    protein_profile.add_right(ma.plotter.Numbers(cells_count, color="#B80000"), pad=0.1)
    # 热图标题
    protein_profile.add_title("Proteomics Profile", fontsize=16)
    # 两张热图 排版合并
    comb = gene_profile + protein_profile
    # 图注添加在top
    comb.add_legends("top", stack_size=1, stack_by="column", align_stacks="top")
    # 最终渲染
    comb.render()
    # 保存图片
    comb.save("MultiOmics.png")
