import seaborn as sns
import pandas as pd
import numpy as np

# 读取数据
data = pd.read_csv('output_data2.csv')

# 定义需要处理的数据列列表
cols_to_process = ['NumericFeature3','NumericFeature4','NumericFeature5','NumericFeature6']

for col in cols_to_process:
    # 计算箱线图参数
    Q1 = np.percentile(data[col], 25)
    Q3 = np.percentile(data[col], 75)
    IQR = Q3 - Q1

    # 确定异常值的阈值
    threshold = 1.5 * IQR

    # 确定异常值的位置
    outliers = data[(data[col] < Q1 - threshold) | (data[col] > Q3 + threshold)][col]

    # 将异常值替换为均值
    data[col] = data[col].replace({outlier: data[col].mean() for outlier in outliers})

# 将处理后的数据保存到新文件
data.to_csv('processed_output_data2.csv', index=False)