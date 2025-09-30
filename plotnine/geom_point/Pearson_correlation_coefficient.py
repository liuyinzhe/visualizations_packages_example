import re
import pandas as pd
from pathlib import Path

import numpy as np
from plotnine import ggplot, aes, geom_point, geom_smooth, annotate, theme_bw
from scipy import stats


def draw(species_name,qct_ord_lst,species_abun_lst,outdir):
    png_path = outdir.joinpath(species_name+".png")
    pdf_path = outdir.joinpath(species_name+".pdf")

    data = pd.DataFrame({
        'QCT': qct_ord_lst,
        'abundance': species_abun_lst
    })

    #计算相关系数 R² 和 p 值
    slope, intercept, r_value, p_value, std_err = stats.linregress(data['QCT'], data['abundance'])
    r_squared = r_value**2
    if p_value < 0.05:
        # 构建标注文本
        # 使用格式化的字符串,保留两位小数。注意p值的显示方式。
        label_text = f'R² = {r_squared:.2f}\np = {p_value:.4f}'

        # 绘制图形
        base_plot = (ggplot(data, aes(x='QCT', y='abundance'))
                    + geom_point(color='blue', alpha=0.6)  # 绘制散点
                    + geom_smooth(method='lm', se=True, color='red', fill='lightpink', alpha=0.3)  # 添加线性回归线和置信区间
                    + annotate('text', x=data['QCT'].min(), y=data['abundance'].max(),  # 在左上角添加标注
                                label=label_text, ha='left', va='top', size=10, color='darkred')
                    + theme_bw()  # 设置主题
                    )


        base_plot.save(filename=png_path, width=10, height=6, dpi=300)
        base_plot.save(filename=pdf_path, width=10, height=6)
    return r_value,r_squared,p_value


def main():
    pwd = Path.cwd()
    outdir = pwd.joinpath("images")
    outdir.mkdir(parents=True,exist_ok=True)

    # raw_sample_name_lst = [
    #     'C86', 'C83', 'C82', 'C81', 'C80', 'C79', 'C78', 'C77', 'C76', 'C75', 'C73', 'C72', 'C71', 'C70', 'C69',
    #     'A11', 'A10', 'A9', 'A8', 'A7', 'A6', 'A5', 'A4', 'A3-1', 'A3', 'A2', 'A1'
    # ]
    df = pd.read_excel("工作簿1.xlsx",dtype=str)
    sample_qct_dic = {}
    qct_sample_lst = []
    for index, row in df.iterrows():
        #print(index)
        sample_name = row["group"].strip()
        qct_value = float(row["QCT"])
        if sample_name not in sample_qct_dic:
            sample_qct_dic[sample_name] = qct_value
        else:
            print("Warnning!")
        qct_sample_lst.append([qct_value,sample_name])
    
    sorted_qct_sample_lst = sorted(qct_sample_lst,key=lambda x:x[0],reverse=False)
    sample_ord_lst = [x[1] for x in sorted_qct_sample_lst]
    qct_ord_lst = [x[0] for x in sorted_qct_sample_lst]

    result_dic = {} # species:{sample:value}
    sample_index_dic = {}
    with open("species_abundance.txt",mode='rt',encoding='utf-8') as fh:
        for line in fh:
            record = re.split("\t+?",line.strip())
            if line.startswith("clade_name"):
                for index in range(len(record)):
                    if index == 0:
                        continue
                    sample_index_dic[record[index]] = index # 样品名对应index
                continue
            species_name = re.split("\|",record[0])[-1]
            if species_name not in result_dic:
                result_dic[species_name] = []
            for sample_name in sample_ord_lst:
                idx = sample_index_dic[sample_name]
                abundance = float(record[idx])
                result_dic[species_name].append(abundance) # 按照顺序
    with open("result.xls",mode="wt",encoding='utf-8') as out:
        out.write("species_name\tr_value\tr_squared\tp_value\n")
        for species_name,abundance_lst in result_dic.items():
            r_value,r_squared,p_value = draw(species_name,qct_ord_lst,abundance_lst,outdir)
            out.write("\t".join(list(map(str,[species_name,r_value,r_squared,p_value])))+'\n')



if __name__ == "__main__":
    main()
