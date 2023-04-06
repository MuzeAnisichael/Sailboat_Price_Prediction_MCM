import pandas as pd

# 读取Excel文件
excel_file = 'datalist2.xlsx'  # 替换为你的Excel文件名
sheet_name = 'Monohulled'  # 替换为你需要处理的工作表名
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# 遍历每一列，并处理数据
for col in df.iloc[:, 8:16]:  # 如果列索引是从0开始的，I列至P列对应的索引范围是8-15
    # 将字符串数字转换为数字
    df[col] = pd.to_numeric(df[col], errors='coerce')

    # 计算非0值的平均值
    non_zero_mean = df[df[col] != 0][col].mean()

    # 将0值替换为非0值的平均值
    df[col] = df[col].replace(0, non_zero_mean)

# 保存处理后的数据到新的Excel文件
output_file = 'processed_' + excel_file
df.to_excel(output_file, index=False, engine='openpyxl')
