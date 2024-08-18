

import numpy as np
import matplotlib.pyplot as plt
import marsilea as ma
import marsilea.plotter as mp
# from marsilea.plotter import TextMesh
# from marsilea.plotter import ColorMesh

color_data = np.random.randint(0, 10, (10, 10))
text_data = np.random.randint(0, 10, (10, 10))

color_mesh = mp.ColorMesh(color_data, annot=False)
text_mesh = mp.TextMesh(text_data)

# # 白板
wb = ma.WhiteBoard(width=3, height=3, margin=0.2)
# 添加图层
wb.add_layer(color_mesh)
wb.add_layer(text_mesh)
wb.save("heatmap_add_layer_text.png")
#plt.savefig("heatmap_add_Range.png", bbox_inches="tight")

# Mesh 输入数据为 np.ndarray
# np.ndarray  与 dataframe 互相转换
'''
# 通过values方法，实现dataframe转换为ndarray
import pandas as pd
 
data = [['2019/08/01', 10],
        ['2019/08/01', 11]]
result = pd.DataFrame(data, columns=['ds', 'val'])
result.values


# series转换为ndarray
import pandas as pd
 
data = [['2019/08/01', 10],
        ['2019/08/01', 11]]
result = pd.DataFrame(data, columns=['ds', 'val'])
result['val'].values
 
data2 = pd.Series([1, 2, 3])
data2.values

# ndarray 转换为 series 通过map结合lamdba
# 只取了 第一列作为 list
import numpy as np
import pandas as pd
 
data = np.array([1, 2, 3]).reshape(3, 1)
data_list = map(lambda x: x[0], data)
ser = pd.Series(data_list)


# ndarray转换为dataframe

import numpy as np
import pandas as pd
 
data = np.array([['2019/08/02', 'zhansan', 1], ['2019/08/03', 'lisi', 2], ['2019/08/04', 'wangwu', 3]])
df = pd.DataFrame(data)


# 代码参考自:https://blog.csdn.net/qq_33873431/article/details/98077676
'''
