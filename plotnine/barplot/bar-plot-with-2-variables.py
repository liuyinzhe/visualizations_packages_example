import pandas as pd

from plotnine import (
    ggplot,
    aes,
    geom_col,
    geom_text,
    position_dodge,
    lims,
    theme,
    element_text,
    element_blank,
    element_rect,
    element_line,
)
# https://plotnine.org/gallery/bar-plot-with-2-variables.html

df = pd.DataFrame(
    {
        "variable": [
            "gender",
            "gender",
            "age",
            "age",
            "age",
            "income",
            "income",
            "income",
            "income",
        ],
        "category": [
            "Female",
            "Male",
            "1-24",
            "25-54",
            "55+",
            "Lo",
            "Lo-Med",
            "Med",
            "High",
        ],
        "value": [60, 40, 50, 30, 20, 10, 25, 25, 40],
    }
)
print(df)
# 指定分类变量 pd.Categorical 
df["variable"] = pd.Categorical(df["variable"], categories=["gender", "age", "income"])  # categories 为变量顺序
df["category"] = pd.Categorical(df["category"], categories=df["category"])
#categories=df["category"]，这意味着将当前列中出现的所有值（包括重复值）作为分类的类别
#分类的顺序是数据中第一次出现的顺序，而不是按字母顺序或任何其他排序

print(df)

dodge_text = position_dodge(width=0.9)


fig=(
    ggplot(df, aes(x="variable", y="value", fill="category"))
    + geom_col(stat="identity", position="dodge", show_legend=False)
    + geom_text(
        aes(y=-0.5, label="category"),
        position=dodge_text,
        color="gray",
        size=8,
        angle=45,
        va="top",
    )
    + geom_text(
        aes(label="value"),  # new
        position=dodge_text,
        size=8,
        va="bottom",
        format_string="{}%",
    )
    + lims(y=(-5, 60))
)
# print(dir(a))

# 保存为一个高分辨率的PNG图片
fig.save(filename='high_res_plot.png', width=10, height=6, dpi=300)

# 保存为PDF矢量图，适合学术出版
fig.save(filename='vector_plot.pdf', width=10, height=6)
