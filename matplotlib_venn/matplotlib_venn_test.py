import re
import matplotlib.pyplot as plt
from matplotlib_venn import venn2,venn2_circles
from matplotlib_venn import venn3,venn3_circles

#import matplotlib
#matplotlib.rc("font",family='SimSun')
plt.rc('font',family='SimSun') 

# YouYuan 幼圆字体
# SimHei 微软雅黑
# SimSun 宋体
# KaiTi 楷体
# Microsoft YaHei 微软雅黑
# Microsoft JhengHei 微软正黑
# Adobe Fangsong Std 仿宋
# Adobe Heiti Std 黑体
# Adobe Kaiti Std 楷体

# 字体和font-family对照表
# https://blog.csdn.net/lunhui1994_/article/details/80507970


#  # 查询当前系统所有字体
# from matplotlib.font_manager import FontManager
# import subprocess

# mpl_fonts = set(f.name for f in FontManager().ttflist)

# print('all font list get from matplotlib.font_manager:')
# for f in sorted(mpl_fonts):
#     print('\t' + f)



A_set = set()
B_set = set()
with open('input.tsv',mode='rt',encoding='utf-8') as fh:
    for line in fh:
        record = re.split('\t',line.strip())
        if line.startswith('流程'):
            continue
        A_set.add(record[0])
        B_set.add(record[1])
total = len(A_set.union(B_set)) # 共有的数量
venn_data = [A_set,B_set]
venn2_diagram = venn2(venn_data,
          set_labels = ('批量    ', '    人工'),
          subset_label_formatter=lambda x: f"{x}\n{(x/total):1.0%}" # 数字\n百分比
          )
# 添加标题
plt.title("标题", loc='center')
# 展示
#plt.show()
# 保存
plt.savefig('venn_plot.png',dpi=600)

# 参考
# https://github.com/konstantint/matplotlib-venn
# https://blog.csdn.net/LuohenYJ/article/details/103091081
# https://zhuanlan.zhihu.com/p/566505361
# 彻底解决Python里matplotlib不显示中文的问题
# https://zhuanlan.zhihu.com/p/104081310
