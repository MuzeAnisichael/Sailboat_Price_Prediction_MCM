# %matplotlib inline
import pandas as pd
import random
import torch
import d2l
'''
# 定义线性模型函数
# """⽣成y=Xw+b+噪声"""
def synthetic_data(w, b, num_examples):
    X = torch.normal(0, 1, (num_examples, len(w)))
    # X是从0到1由正态分布随机生成的矩阵，行数为特征数，列数和模型权重w相同
    y = torch.matmul(X, w) + b
    # y是特征X和模型权重w的矩阵-向量乘法后加上偏置b（向量）
    y += torch.normal(0, 0.01, y.shape)
    #y 加上噪声项，模拟真实样本点
    return X, y.reshape((-1, 1))
'''

'''

# 给定真实的模型权重w和偏置b
true_w = torch.tensor([2, -3.4])
true_b = 4.2
# 调用函数生成数据集
features, labels = synthetic_data(true_w, true_b, 1000)
'''

data = pd.read_excel("2023_MCM_Problem_Y_Boats.xlsx" , sheet_name = "Monohulled")

num = 500

yy = pd.DataFrame(data).iloc[0:num,5]
x1 = pd.DataFrame(data).iloc[0:num,7]
x2 = pd.DataFrame(data).iloc[0:num,8]

x1_tensor = torch.tensor(x1, dtype=torch.float32).view(-1, 1)
x2_tensor = torch.tensor(x2, dtype=torch.float32).view(-1, 1)


y_tensor = torch.tensor(yy, dtype=torch.float32).view(-1, 1)
x_tensor = torch.stack((x1_tensor, x2_tensor))


# 读取数据集
def data_iter(batch_size, features, labels):
    num_examples = len(features)
    indices = list(range(num_examples))
# 这些样本是随机读取的，没有特定的顺序
    random.shuffle(indices)
    for i in range(0, num_examples, batch_size):
        batch_indices = torch.tensor(
            indices[i: min(i + batch_size, num_examples)])
        yield features[batch_indices], labels[batch_indices]

# 初始化模型参数
w = torch.normal(0, 0.01, size=(2,1), requires_grad=True)
b = torch.zeros(1, requires_grad=True)

# 定义模型
# """线性回归模型"""
def linreg(X, w, b): 
    return torch.matmul(X, w) + b

# 定义损失函数
# """均⽅损失"""
def squared_loss(y_hat, y):
    return (y_hat - y.reshape(y_hat.shape)) ** 2 / 2

# 定义优化算法
# """⼩批量随机梯度下降"""
def sgd(params, lr, batch_size):
    with torch.no_grad():
        for param in params:
            param -= lr * param.grad / batch_size
            param.grad.zero_()


# 训练
lr = 0.03
num_epochs = 5
batch_size =30
net = linreg
loss = squared_loss

for epoch in range(num_epochs):
    for X, y in data_iter(batch_size, x_tensor, y_tensor):
        l = loss(net(x_tensor, w, b), y_tensor) # X和y的⼩批量损失
        # 因为l形状是(batch_size,1)，⽽不是⼀个标量。l中的所有元素被加到⼀起，
        # 并以此计算关于[w,b]的梯度
        l.sum().backward()
        sgd([w, b], lr, batch_size) # 使⽤参数的梯度更新参数
    with torch.no_grad():
        train_l = loss(net(x_tensor, w, b), y_tensor)
        print(f'epoch {epoch + 1}, loss {float(train_l.mean()):f}')