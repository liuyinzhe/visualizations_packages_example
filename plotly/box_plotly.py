import plotly
# import plotly.express as px
# import pandas as pd
import numpy  as np
import plotly.graph_objects as go
import os
import re
from pathlib import Path
import gzip
# 跳转脚本所在目录
pwd = os.path.split(os.path.realpath(__file__))[0]
pwd = Path(pwd)
os.chdir(pwd) 


# 获取df
sample_lst = ["A","B","C"]
sample_depth_dic = {} # k 样品名， value 数值
for sample in sample_lst:
    if sample not in sample_depth_dic:
        sample_depth_dic[sample] = []
    
    with gzip.open(sample+'.region.tsv.gz',mode='rt',encoding='utf-8') as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            record = re.split("\t",line.strip())
            depth_value = float(record[3])
            sample_depth_dic[sample].append(depth_value)
    

# print(cancer_type_tmb_dic)
N = len(sample_lst)
colors = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]
y_data = [sample_depth_dic[x] for x in sample_lst ]
#print(y_data)
fig = go.Figure()

for xd, yd, cls in zip(sample_lst, y_data, colors):
        fig.add_trace(go.Box(
            y=yd,
            name=xd,
            boxpoints='all',
            jitter=0.5,
            whiskerwidth=0.2,
            fillcolor=cls,
            marker_size=2,
            line_width=1)
        )

fig.update_layout(
    title='The depth distribution of target area',
    yaxis=dict(
        autorange=True,
        showgrid=True,
        zeroline=True,
        dtick=5,
        gridcolor='rgb(255, 255, 255)',
        gridwidth=1,
        zerolinecolor='rgb(255, 255, 255)',
        zerolinewidth=2,
    ),
    margin=dict(
        l=40,
        r=30,
        b=80,
        t=100,
    ),
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
    showlegend=False
)



# 网页方式预览
#fig = px.box(df, y="total_bill",points="all")
# fig.show()



# 保存到html
# Representation of figure as an HTML div string
# https://plotly.com/python-api-reference/generated/plotly.io.to_html.html
html_str = plotly.io.to_html(fig)
with open("depth_distribution.html",mode='w',encoding='utf-8') as out:
    out.write(html_str)
    
