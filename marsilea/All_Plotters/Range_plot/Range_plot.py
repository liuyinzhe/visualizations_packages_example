from marsilea.plotter import Range

import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import pyplot as plt

_, ax = plt.subplots()
'''
numpy.random.randint(low, high=None, size=None, dtype='l')

参数	说明
low	生成的整数最低值（包含），即所有生成的整数都会大于等于这个值。
high	生成的整数最高值（不包含），即所有生成的整数都会小于这个值。
size	输出的形状，可以为整数（生成元素的数量）或者元组（各维度的大小）。如果不提供，则返回一个单一随机整数。
dtype	数据类型，可选参数，默认为’l’，表示生成的数据类型为整数。
'''
data = np.random.randint(low=1, high=100, size=(10, 2))  # 10行2列
'''
print(data) #
[[ 9 98]
 [62 39]
 [23  2]
 [31 82]
 [73 93]
 [20 97]
 [97 76]
 [27 65]
 [ 9 40]
 [ 4 17]]
'''
Range(data).render(ax)



# 保存图片
plt.savefig("Range_plot.png", bbox_inches="tight")




import marsilea as ma
import numpy as np
data = np.random.rand(10, 2)
range_data = np.random.randint(1, 100, (10, 2))
h = ma.Heatmap(data,name="heatmap")
h.add_left(ma.plotter.Range(range_data, items=["A", "B"]),name='range')



h.render()
'''
# https://marsilea.readthedocs.io/en/stable/tutorial/axes-level.html
No axes or figure is created or render until you call the render() method.
After you render the visualization, you can access the main axes by get_main_ax().
'''
#print(type(h))
# <class 'marsilea.heatmap.Heatmap'>
#main_ax = h.get_main_ax()
#print(main_ax)

# 获得axis 设置x 轴，避免官方图片中突变不完整,或者太近的问题
range_ax = h.get_ax("range")
range_ax.set_xlim(0, 120) # y轴 限制最大值 
#range_ax.set_xticks([120]) # 设置y轴刻度只显示最大值

#h.save("heatmap_add_Range.png")
#plt.savefig("heatmap_add_Range.png", bbox_inches="tight")
plt.savefig("heatmap_add_Range.png")
