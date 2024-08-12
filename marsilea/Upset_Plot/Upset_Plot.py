from matplotlib import pyplot as plt

import marsilea as ma
from marsilea.upset import UpsetData


imdb = ma.load_data("imdb")
'''
print(imdb)
     Rank                    Title                     Genre  ...   Votes Revenue (Millions) Metascore
0       1  Guardians of the Galaxy   Action,Adventure,Sci-Fi  ...  757074             333.13        76
1       2               Prometheus  Adventure,Mystery,Sci-Fi  ...  485820             126.46        65
2       3                    Split           Horror,Thriller  ...  157606             138.12        62
3       4                     Sing   Animation,Comedy,Family  ...   60545             270.32        59
4       5            Suicide Squad  Action,Adventure,Fantasy  ...  393727             325.02        40
..    ...                      ...                       ...  ...     ...                ...       ...
994   996     Secret in Their Eyes       Crime,Drama,Mystery  ...   27585               0.00        45
995   997          Hostel: Part II                    Horror  ...   73152              17.54        46
996   998   Step Up 2: The Streets       Drama,Music,Romance  ...   70699              58.01        50
997   999             Search Party          Adventure,Comedy  ...    4881               0.00        22
998  1000               Nine Lives     Comedy,Family,Fantasy  ...   12435              19.64        11

[999 rows x 12 columns]
'''
items_attrs = imdb[
    [
        "Title",
        "Year",
        "Runtime (Minutes)",
        "Rating",
        "Votes",
        "Revenue (Millions)",
        "Metascore",
    ]
].set_index("Title")

'''
print(items_attrs)
# 取了额外列信息 "Revenue (Millions)" 做分布散点图
# 取了额外列信息 "Rating" 做了箱式图
                         Year  Runtime (Minutes)  Rating   Votes  Revenue (Millions)  Metascore
Title
Guardians of the Galaxy  2014                121     8.1  757074              333.13         76
Prometheus               2012                124     7.0  485820              126.46         65
Split                    2016                117     7.3  157606              138.12         62
Sing                     2016                108     7.2   60545              270.32         59
Suicide Squad            2016                123     6.2  393727              325.02         40
...                       ...                ...     ...     ...                 ...        ...
Secret in Their Eyes     2015                111     6.2   27585                0.00         45
Hostel: Part II          2007                 94     5.5   73152               17.54         46
Step Up 2: The Streets   2008                 98     6.2   70699               58.01         50
Search Party             2014                 93     5.6    4881                0.00         22
Nine Lives               2016                 87     5.3   12435               19.64         11

[999 rows x 6 columns]
'''

'''
marsilea.upset.UpsetData.from_memberships()
# items  [groupA,groupB，groupC]
# items_names  统计的元素
Parameters:
      items
            array of array of sets_names, dict
            The data of items

      items_names
            optional
            The name of items, if name is not provided, it will be automatically named as “Item 1, Item 2, …”

      sets_attrs
            optional, pd.DataFrame
            The attributes of sets, the input index should be the same as sets_names

      items_attrs
            optional, pd.DataFrame
            The attributes of items, the input index should be the same as items
'''

upset_data = UpsetData.from_memberships(
    imdb.Genre.str.split(","), items_names=imdb["Title"], items_attrs=items_attrs
)

# 第二种读取例子
#marsilea.upset.UpsetData.from_sets()
'''
Parameters:

sets
    array of sets, dict
    The sets data

sets_names
    optional
    The name of sets, if name is not provided, it will be automatically named as “Set 1, Set 2, …”

sets_attrs
    optional, pd.DataFrame
    The attributes of sets, the input index should be the same as sets_names

items_attrs
    optional, pd.DataFrame
    The attributes of items, the input index should be the same as items
'''
'''

from marsilea.upset import UpsetData, Upset
data = UpsetData.from_sets(sets=[[1, 2, 3, 4],
                            [3, 4, 5, 6],
                            [1, 6, 10, 11]]
                       , sets_names=["setA", "setB", "setC"])
us = Upset(data)
us.render()
us.save("Upset_Plot.png")
'''

# Upset Plot
# marsilea.upset.Upset
# orientstr: The orientation of the Upset plot
# min_cardinality: Select a fraction of subset to render by cardinality
us = ma.upset.Upset(upset_data, orient="v", min_cardinality=15)

# Highlight a subset of the data
us.highlight_subsets(min_cardinality=48, facecolor="#D0104C", label="Larger than 48")
us.highlight_subsets(
    min_cardinality=32, edgecolor="green", edgewidth=1.5, label="Larger than 32"
)

# Add a plot for the items attribute
# 添加绘图属性,在一测绘图
'''
Add a plot for the items attribute
Parameters:
    side
    str
    The side to add the plot, can be ‘left’, ‘right’, ‘top’, ‘bottom’
attr_name
    str
    The name of the attribute
plot
    str
    The type of plot, can be ‘bar’, ‘box’, ‘boxen’, ‘violin’, ‘point’, ‘strip’, ‘swarm’, ‘stack_bar’, ‘number’
name
    str, optional
    The name of the plot
pad
    float, optional
    The padding between the plot and the axis
size
    float, optional
    The size of the plot
plot_kws
    dict, optional
    The keyword arguments for the plot
'''
us.add_items_attr(
    "left", # 位置
    "Revenue (Millions)", # 标题
    "strip", # 分类散点图stripplot()
    pad=0.2,
    size=0.5,
    plot_kws=dict(color="#24936E", size=1.2, label="Revenue\n(Millions)"),
)
us.add_items_attr(
    "right",  # 位置
    "Rating", # 标题
    "box",  # 箱式图
    pad=0.2,
    plot_kws=dict(color="orange", linewidth=1, fliersize=1),
)
# 添加图注
# box_padding: Add pad around the whole legend box
us.add_legends(box_padding=0)
# 设置边框
us.set_margin(0.3)
# 最终渲染
us.render()

us.save("Upset_Plot.png")
