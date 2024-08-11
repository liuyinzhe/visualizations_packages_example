from collections import Counter
import numpy as np
import pandas as pd

import marsilea as ma
import matplotlib as mpl


seq = ma.load_data("seq_align")
seq.to_csv("seq_align.tsv",sep='\t')
#print(type(seq))
# 拆分取130-175列
seq = seq.iloc[:, 130:175]

# Calculate the height of each amino acid.

collect = []
# 统计每个位置的碱基类型计数
for _, col in seq.items():
    '''print(col)
    Name: 453, dtype: object
    PH4H_Rattus_norvegicus            K
    PH4H_Mus_musculus                 K
    PH4H_Homo_sapiens                 K
    PH4H_Bos_taurus                   K
    PH4H_Chromobacterium_violaceum    -
    PH4H_Ralstonia_solanacearum       -
    PH4H_Caulobacter_crescentus       -
    PH4H_Pseudomonas_aeruginosa       -
    PH4H_Rhizobium_loti               -

    '''
    collect.append(Counter(col))

'''
print(collect)
[Counter({'-': 5, 'M': 4}), Counter({'-': 5, 'A': 2, 'S': 2}), Counter({'-': 5, 'A': 3, 'T': 1}), Counter({'-': 5, 'V': 2, 'A': 1, 'L': 1}), Counter({'-': 5, 'V': 4})]
'''
hm = pd.DataFrame(collect)
del hm["-"]
# na 填充0.0
hm = hm.T.fillna(0.0)
hm.columns = seq.columns
# 求百分比
hm /= hm.sum(axis=0)

n = hm.shape[1]
s = 20
En = (1 / np.log(2)) * ((s - 1) / (2 * n))

heights = []
for _, col in hm.items():
    # 对于等于0的情况转为 极小值,避免报错 RuntimeWarning: divide by zero encountered in log2.
    col[col == 0] = 1e-100
    H = -(np.log2(col) * col).sum()
    R = np.log2(20) - (H + En)
    heights.append(col * R)

logo = pd.DataFrame(heights).T

#print(logo)
'''
          0         1         2         3         4  ...       451       452       453       454       455
M  4.291872  0.000000  0.000000  0.000000  0.000000  ...  0.000000  0.000000  0.000000  0.000000  0.000000
A  0.000000  1.645936  2.610445  0.697968  0.000000  ...  0.713989  0.000000  0.000000  0.000000  0.000000
S  0.000000  1.645936  0.000000  0.000000  0.000000  ...  0.000000  0.000000  0.000000  0.000000  4.291872
T  0.000000  0.000000  0.870148  0.000000  0.000000  ...  0.000000  0.000000  0.000000  0.000000  0.000000
V  0.000000  0.000000  0.000000  1.395936  4.291872  ...  0.000000  0.000000  0.000000  0.000000  0.000000
W  0.000000  0.000000  0.000000  0.000000  0.000000  ...  0.000000  0.000000  0.000000  0.000000  0.000000

[20 rows x 456 columns]
'''


# Prepare color palette and data

color_encode = {
    "A": "#f76ab4",
    "C": "#ff7f00",
    "D": "#e41a1c",
    "E": "#e41a1c",
    "F": "#84380b",
    "G": "#f76ab4",
    "H": "#3c58e5",
    "I": "#12ab0d",
    "K": "#3c58e5",
    "L": "#12ab0d",
    "M": "#12ab0d",
    "N": "#972aa8",
    "P": "#12ab0d",
    "Q": "#972aa8",
    "R": "#3c58e5",
    "S": "#ff7f00",
    "T": "#ff7f00",
    "V": "#12ab0d",
    "W": "#84380b",
    "Y": "#84380b",
    "-": "white",
}

max_aa = []
freq = []

for _, col in hm.items():
    '''
    print(col)
    Name: 452, dtype: float64
    M    0.00
    A    0.00
    S    0.00
    T    0.00
    V    0.00
    L    0.25
    E    0.00
    N    0.00
    G    0.00
    P    0.00
    R    0.00
    K    0.00
    D    0.00
    F    0.00
    Q    0.00
    Y    0.00
    I    0.75
    C    0.00
    H    0.00
    W    0.00
    '''
    # np.argmax是用于取得数组中每一行或者每一列的的最大值
    '''
    one_dim_array = np.array([1, 4, 5, 3, 7, 2, 6])
    print(np.argmax(one_dim_array))
    运算后,降一维,成为一个数值,7的索引值维4,所以运算结果:4
    '''
    # 获得最大值的行索引
    ix = np.argmax(col)
    max_aa.append(hm.index[ix])
    freq.append(col.iloc[ix])

# 被10 整除的区间，不显示的则用""占位
position = [] # 位置坐标
mock_ticks = []  # 注释内容
for i in seq.columns:
    if int(i) % 10 == 0:
        position.append(i)
        mock_ticks.append("^")
    else:
        position.append("")
        mock_ticks.append("")


# Plot
height = 5
width = height * seq.shape[1] / seq.shape[0]
# 分类热图
# Categorical Heatmap
ch = ma.CatHeatmap(seq.to_numpy(), palette=color_encode, height=height, width=width)

# The mesh that draw text on each cell
# 在热图每个cell 中添加文字
ch.add_layer(ma.plotter.TextMesh(seq.to_numpy()))

# Sequence logo
# 上方的大小文字,对应出现频次多少 整体信息熵低的频次高,文字大
ch.add_top(ma.plotter.SeqLogo(logo, color_encode=color_encode), pad=0.1, size=2)

# 左侧的序列名字标签
ch.add_left(ma.plotter.Labels(seq.index), pad=0.1)

# 位置信息添加 
ch.add_bottom(ma.plotter.Labels(mock_ticks, rotation=0), pad=0.1)
ch.add_bottom(ma.plotter.Labels(position, rotation=0))

# 添加底部的数量统计柱状图,并且给定了组件名字freq_bar;可以用来控制add_legends()指定图例顺序
ch.add_bottom(
    ma.plotter.Numbers(freq, width=0.9, color="#FFB11B", show_value=False),
    name="freq_bar",
    size=2,
)
# 底部标签
ch.add_bottom(ma.plotter.Labels(max_aa, rotation=0), pad=0.1)
# 最终渲染
ch.render()

# 设置 底部的 freq_bar 关闭刻度显示;似乎没有效果
ch.get_ax("freq_bar").set_axis_off()

ch.save("Sequence_Alignment_Plot.png")
