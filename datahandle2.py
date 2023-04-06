import pandas as pd

# 读取Excel文件
excel_file = "2023_MCM_Problem_Y_Boats.xlsx"  # 请替换为您的Excel文件路径
sheet_name = "Sheet1"  # 请替换为您的工作表名称
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# 创建新的“Id”列
id_col = pd.Series(range(1, len(df) + 1), name='Id')

# 选取所需的列
price = df.iloc[:, 5]
numeric_features = df.iloc[:, 8:18]
category_feature = df.iloc[:, 0]

# 合并所需的列并为其分配列名
output_data = pd.concat([id_col, price, numeric_features, category_feature], axis=1)
output_data.columns = ['Id'] + ['Price'] + [f'NumericFeature{i + 1}' for i in range(10)] + ['CategoryFeature']

# 将合并后的数据输出到CSV文件
output_data.to_csv("hongkong.csv", index=False)
