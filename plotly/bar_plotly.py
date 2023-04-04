import plotly
import plotly.express as px
import pandas as pd


data_dic={     
'sample':["A","B","C"],
'mapping_rate':[34.35,35.69,33.49]
}




df = pd.DataFrame(data_dic)

fig = px.bar(
    df, # 数据集
    x='sample', # x轴
    y='mapping_rate', # y轴
)
# fig.show()

# Representation of figure as an HTML div string
html_str = plotly.io.to_html(fig)
# https://plotly.com/python-api-reference/generated/plotly.io.to_html.html

with open("bar.html",mode='w',encoding='utf-8') as out:
    out.write(html_str)
    
