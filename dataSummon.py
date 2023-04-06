import pandas as pd
import numpy as np

# 创建模拟数据
num_samples = 1000

# 特征数据
synthetic_features = pd.DataFrame({
    'Make': np.random.choice(['A', 'B', 'C'], num_samples),
    'Variant': np.random.choice(['X', 'Y', 'Z'], num_samples),
    'x1': np.random.rand(num_samples) * 100,
    'x2': np.random.rand(num_samples) * 1000,
    'x3': np.random.rand(num_samples) * 10000
})

synthetic_features.to_csv("synthetic_features.csv", index=False)

# 价格数据
synthetic_prices = pd.DataFrame({
    'Listing_Price': np.random.rand(num_samples) * 100000
})

synthetic_prices.to_csv("synthetic_prices.csv", index=False)

# 测试特征数据
your_test_features = pd.DataFrame({
    'Make': np.random.choice(['A', 'B', 'C'], num_samples),
    'Variant': np.random.choice(['X', 'Y', 'Z'], num_samples),
    'x1': np.random.rand(num_samples) * 100,
    'x2': np.random.rand(num_samples) * 1000,
    'x3': np.random.rand(num_samples) * 10000
})

your_test_features.to_csv("your_test_features.csv", index=False)

# 测试价格数据
your_test_prices = pd.DataFrame({
    'Listing_Price': np.random.rand(num_samples) * 100000
})

your_test_prices.to_csv("your_test_prices.csv", index=False)
