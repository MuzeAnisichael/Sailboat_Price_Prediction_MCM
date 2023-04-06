import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, LassoCV
from sklearn.metrics import mean_squared_error
import xgboost as xgb

# 创建模拟数据集
data = pd.DataFrame(np.random.rand(3000, 13), columns=[f'x{i}' for i in range(1, 14)])
data['Company'] = np.random.choice(['A', 'B', 'C', 'D', 'E'], size=3000)
data['Price'] = np.random.rand(3000)

# 将公司列进行独热编码
data = pd.get_dummies(data)

# 划分数据集为训练集和测试集
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# 提取特征和标签
X_train = train_data.drop('Price', axis=1)
y_train = train_data['Price']
X_test = test_data.drop('Price', axis=1)
y_test = test_data['Price']

# 创建并拟合Ridge回归模型
model_ridge = Ridge(alpha=1.0)
model_ridge.fit(X_train, y_train)

# 输出Ridge回归模型的参数
print("Ridge Model Parameters:")
print(model_ridge.get_params())

# 创建并拟合Lasso回归模型
model_lasso = LassoCV(alphas=[1, 0.1, 0.001, 0.0005])
model_lasso.fit(X_train, y_train)

# 输出Lasso回归模型的参数
print("\nLasso Model Parameters:")
print(model_lasso.get_params())

# 创建并拟合XGBoost模型
model_xgb = xgb.XGBRegressor(n_estimators=360, max_depth=2, learning_rate=0.1)
model_xgb.fit(X_train, y_train)

# 输出XGBoost模型的参数
print("\nXGBoost Model Parameters:")
print(model_xgb.get_params())

# 预测和评估模型
ridge_preds = model_ridge.predict(X_test)
lasso_preds = model_lasso.predict(X_test)
xgb_preds = model_xgb.predict(X_test)

# 计算均方误差（MSE）
ridge_mse = mean_squared_error(y_test, ridge_preds)
lasso_mse = mean_squared_error(y_test, lasso_preds)
xgb_mse = mean_squared_error(y_test, xgb_preds)

print(f'\nRidge MSE: {ridge_mse}')
print(f'Lasso MSE: {lasso_mse}')
print(f'XGBoost MSE: {xgb_mse}')

# 输出Lasso回归系数矩阵和截距
print("Lasso回归系数矩阵：")
print(model_lasso.coef_)
print("Lasso回归截距：")
print(model_lasso.intercept_)

# 输出Ridge回归系数矩阵和截距
print("Ridge回归系数矩阵：")
print(model_ridge.coef_)
print("Ridge回归截距：")
print(model_ridge.intercept_)