# pip install pyBigWig
# pip install mpl_fontkit
# tracks = ma.load_data("track")
# https://github.com/Marsilea-viz/marsilea/blob/main/scripts/example_figures/tracks.py
# 
# Please downlaod data from https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE137105

# https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M35/gencode.vM35.chr_patch_hapl_scaff.basic.annotation.gff3.gz

from pathlib import Path

import matplotlib.pyplot as plt
#import mpl_fontkit as fk
import numpy as np
import pandas as pd
import pyBigWig

#fk.install("Lato")

import marsilea as ma
import marsilea.plotter as mp



def add_gene_structure(ax):
    '''
    添加最下面的基因方块
    '''
    import re
    from matplotlib.lines import Line2D

    myc_structure = pd.read_csv("data/MYC.GFF3", sep="\t", comment="#", header=None)
    #myc_structure = myc_structure[myc_structure[2] == "exon"]
    myc_structure = myc_structure[myc_structure[2] == "gene"]

    def extract_id(text):
        #return re.search(r"ID=exon-(.*?)-", text).group(1)
        #return re.search(r"ID=exon(.*?):", text).group(1)
        return re.search(r"gene_id=(.*?);", text).group(1)
    # 第9列 
    # ID=ENSMUSG00000064842.3;gene_id=ENSMUSG00000064842.3;gene_type=snRNA;gene_name=Gm26206;level=3;mgi_id=MGI:5455983
    myc_structure["id"] = myc_structure[8].apply(extract_id)

    # Skeleton # 骨架
    # _, ax = plt.subplots(figsize=(5, 1))
    ranges = myc_structure[[3, 4]]  # start end
    '''
    print(ranges)
              3        4
    0   3172239  3172348
    3   3276124  3741721
    15  4069780  4479464
    '''
    rmin, rmax = np.min(ranges), np.max(ranges) # 最小的起始值,和最大的终止值
    # 添加长柱子,放置基因方框
    ske = Line2D([rmin, rmax], [0, 0], linewidth=1, color="k") # black,表示黑色,简写为k
    # 手动添加到当前Axes
    ax.add_artist(ske)

    # 3个 gene id,三个颜色
    colors = ["#AF8260", "#E4C59E","#12ab0d"]
    ix = 0
    # 根据id 拆分为多个 dataframe
    for _, df in myc_structure.groupby("id"):
        for _, row in df.iterrows():
            start, end = row[3], row[4]
            #print(start, end)
            e = Line2D([start, end], [0, 0], linewidth=10, color=colors[ix])
            ax.add_artist(e)
        ix += 1

    # ax.set_xlim(MYC_START, MYC_END)
    # 绘制内容缺少第一个基因方块,x轴限制减少后可以了
    ax.set_xlim(MYC_START-225, MYC_END)
    ax.set_ylim(-1, 1)
    ax.set_axis_off()

# Please downlaod data from https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE137105
bws = [i for i in Path("data/GSE137105_RAW/").glob("*.bw")]

# MYC_START = 127734550
# MYC_END = 127744631
MYC_START = 3172018
MYC_END = 4069781

pdata = []
for bw in bws:
    names = bw.stem.split("_") # GSM4066997_shNC_H3K9me1.bw
    bw = pyBigWig.open(str(bw))

    # Gene location of MYC
    # intervals 检索一个范围内的所有区间
    # c:((开始位置、结束位置和值), (开始位置、结束位置和值))
    c = bw.intervals("chr8", MYC_START, MYC_END)
    vs = np.array([i[2] for i in c]) # values 取的数值

    # cond 样品名  enz 环境名 组蛋白
    pdata.append({"cond": names[1], "enz": names[2], "track": vs})

#print(pdata)
pdata = pd.DataFrame(pdata)
'''print(pdata["enz"])
    0    H3K9me1
    1    H3K9me2
    2    H3K9me3
    3      INPUT
    4    H3K9me1
    5    H3K9me2
    6    H3K9me3
    7      INPUT
'''
pdata["enz"] = pdata["enz"].replace("INPUT", "Background")
'''
    print(pdata["enz"])
    0       H3K9me1
    1       H3K9me2
    2       H3K9me3
    3    Background
    4       H3K9me1
    5       H3K9me2
    6       H3K9me3
    7    Background
'''
# 根据两个名字排序,index 重新设置,drop = True  有内容的index 也会被删除,变为纯数字index
pdata = pdata.sort_values(["enz", "cond"]).reset_index(drop=True)

'''
print(pdata)
      cond         enz                                              track
0  shKDM3B  Background  [0.0, 0.5017930269241333, 1.0035899877548218, ...
1     shNC  Background  [0.9526079893112183, 1.4289100170135498, 3.334...
2  shKDM3B     H3K9me1  [0.0, 0.33585700392723083, 0.0, 0.503785014152...
3     shNC     H3K9me1  [0.6501680016517639, 0.32508400082588196, 0.65...
4  shKDM3B     H3K9me2  [0.0, 3.245310068130493, 0.0, 0.54088401794433...
5     shNC     H3K9me2  [0.0, 0.578980028629303, 1.7369400262832642, 2...
6  shKDM3B     H3K9me3  [0.7722370028495789, 0.0, 1.544469952583313, 3...
7     shNC     H3K9me3  [0.0, 0.9895859956741333, 1.9791699647903442, ...
'''

colors = {
    "H3K9me1": "#DD6E42",
    "H3K9me2": "#E8DAB2",
    "H3K9me3": "#4F6D7A",
    "Background": "#C0D6DF",
}

# 设置的y轴最大值
lims = {
    "H3K9me1": 20,
    "H3K9me2": 35,
    "H3K9me3": 35,
    "Background": 20,
}

TRACK_HEIGHT = 0.5 # The size of the plot in inches
TRACK_PAD = 0.1 # # The padding of the plot in inches # 填充
'''
ZeroHeight(width, name=None, margin=0.2) # 宽度,名字,边框保留
A utility class to initialize a canvas with zero height
This is useful when you try to stack many plots

一个实用程序类, 用于初始化高度为零的画布
当您尝试堆叠许多图时，这很有用
'''
# 图中三列 ZeroHeight 空白画布
# myc Area 区域图
myc_track = ma.ZeroHeight(4.5, name="myc")

for _, row in pdata.iterrows():
    track = row["track"]
    name = f"{row['cond']}{row['enz']}"
    color = colors[row["enz"]]
    '''
    class Area(
        data, 
        color=None, 
        add_outline=True, 
        alpha=0.4, 
        linecolor=None, 
        linewidth=1, 
        group_kws=None, 
        label=None, 
        label_loc=None, 
        label_props=None, **kwargs)
    '''
    # 底部添加
    myc_track.add_bottom(
        mp.Area(track, color=color, add_outline=False, alpha=1),
        size=TRACK_HEIGHT, # The size of the plot in inches
        pad=TRACK_PAD, # The padding of the plot in inches # 填充
        name=name,
    )
# 底部添加色块 add_canvas 框架,命名为gene 后面自定义add_gene_structure添加
'''
ax = comp.get_ax("myc", "gene")
add_gene_structure(ax)
'''
myc_track.add_canvas("bottom", name="gene", size=0.2, pad=0.1)
# 添加底部标题
myc_track.add_title(bottom="MYC")

cond_canvas = ma.ZeroHeight(0.8)
for cond in pdata["cond"]:
    '''
    Title(title, align='center',  # {‘center’, ‘left’, ‘right’, ‘bottom’, ‘top’}
        padding=10, fontsize=None, 
        fill_color=None, bordercolor=None, 
        borderwidth=None, borderstyle=None, 
        **options)
    '''
    cond_canvas.add_bottom(
        mp.Title(cond, align="left"), size=TRACK_HEIGHT, pad=TRACK_PAD
    )

enz_canvas = ma.ZeroHeight(1, name="enz")
# 去重
for enz in pdata["enz"].drop_duplicates():
    enz_canvas.add_bottom(
        mp.Title(f"‎ ‎ {enz}", align="left"), # ‎ 空白符，左对齐
        size=TRACK_HEIGHT * 2, # 大小统一一致
        pad=TRACK_PAD * 2, # 大小统一一致
        name=enz,
    )

# 拼图排版
comp = myc_track + 0.1 + cond_canvas + enz_canvas
comp.render()

# Add a line for enz  # 添加右侧 竖的直线
for enz in pdata["enz"].drop_duplicates():
    '''
    marsilea.layout.CompositeCrossLayout
    get_ax(layout_name, ax_name)

    Get a specific axes by name when available
    If the axes is split, multiple axes will be returned
    '''
    ax = comp.get_ax("enz", enz)
    # 垂直线
    ax.axvline(x=0, color="k", lw=4)

for _, row in pdata.iterrows():
    name = f"{row['cond']}{row['enz']}"
    lim = lims[row["enz"]]
    ax = comp.get_ax("myc", name)
    ax.set_ylim(0, lim) # y轴 限制最大值
    ax.set_yticks([lim]) # 设置y轴刻度只显示最大值

# Add gene structure
# get_ax(layout_name, ax_name)
# myc_track = ma.ZeroHeight(4.5, name="myc")
# myc_track.add_canvas("bottom", name="gene", size=0.2, pad=0.1)
ax = comp.get_ax("myc", "gene")
add_gene_structure(ax)

if "__file__" in globals():
    save_path = Path(__file__).parent / "figures"
    save_path.mkdir(exist_ok=True)
    plt.savefig(save_path / "tracks.pdf", bbox_inches="tight")
    plt.savefig(save_path / "tracks.png", bbox_inches="tight") # 绘制内容缺少第一个基因方块,x轴限制减少后可以了
    plt.rcParams["svg.fonttype"] = "none"
    plt.savefig(save_path / "tracks.svg", bbox_inches="tight", facecolor="none")
else:
    plt.show()
