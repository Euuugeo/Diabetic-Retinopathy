# Train

Train：糖尿病性视网膜病变诊断训练代码。

> ***Relevant course***
> * Comprehensive Project in Specialized Direction 2025 (2025年同济大学专业方向综合项目)

## 项目组成

* `/input`
输入眼底原始图像

* `/losses`
存放与模型训练损失相关的数据或文件

* `/output`
输出预测代码

* `/nets`
存放神经网络模型结构的相关代码

* `/weight`

  模型的权重文件

* `DataSet.py`

  一个用于糖尿病性视网膜病变数据集的自定义数据加载器，便于深度学习模型训练和验证。

* `predict-3.py`
糖尿病性视网膜病变诊断预测，生成预测图像。

* `test.py`
测试文件，可以统计模型准确性指标(AUPR,Dice)。

* `train_single_network.py`
训练文件

* `Transforms_v2.py`
实现了医学图像分割任务中常用的数据增强和预处理操作

* `utils.py`
  实现了医学图像分割任务中常用的可视化、张量与numpy互转、AUC/AUPR评估、特征相似度计算、蒸馏损失等实用工具函数和类

* `requirements.txt`
  Python 环境配置文件

数据集太太，因此不放置。

**训练**

```
python train_single_network.py
```

**测试**

```
python test.py
```

