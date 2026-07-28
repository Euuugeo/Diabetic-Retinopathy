# 模型训练、评估与预测

本目录包含糖尿病视网膜病变四类病灶分割所需的数据加载、数据增强、网络结构、损失函数和实验脚本。

## 目录说明

```text
train/
├── input/                    # 示例眼底图像
├── output/                   # 示例预测结果
├── losses/                   # 各模型使用的损失函数
├── nets/                     # 分割网络实现
├── DataSet.py                # IDRiD/DDR 数据集加载
├── Transforms_v2.py          # 数据增强与预处理
├── train_single_network.py   # 单模型训练入口
├── test.py                   # AUPR、Dice 等指标评估
├── predict-3.py              # 单张图像预测与可视化
├── utils.py                  # 指标、张量转换和辅助函数
└── requirements.txt
```

训练后通常还会生成 `single_network_log/` 和 `weight/` 等目录；这些产物未包含在仓库中。

## 环境

推荐配置：

- Python 3.8
- PyTorch 1.13.1
- TorchVision 0.14.1
- CUDA 11.x（可选，但训练推荐使用 GPU）

```bash
cd train
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

`requirements.txt` 是原实验环境的完整快照，其中包含部分较旧或平台相关的软件包。如安装失败，建议先按本机 CUDA/CPU 环境安装 PyTorch，再按脚本实际导入项安装其余依赖。

## 数据集

代码面向 IDRiD 和 DDR 数据集。数据集未随仓库分发，请从官方渠道获取并遵守其许可协议。

训练前请检查 `DataSet.py` 和 `train_single_network.py` 中的数据集路径。当前代码保留了原实验机器的绝对路径，不能在新环境中直接使用。图像与标注需按 `DataSet.py` 中的读取规则组织；标签为背景加 MA、HE、EX、SE 共 5 类。

## 训练

先在 `train_single_network.py` 底部配置：

- `model_name`：模型名称
- `dataset`：`idrid` 或 `ddr`
- `batch_size`、训练轮数等超参数
- 数据集路径、日志路径和可选 checkpoint

然后运行：

```bash
python train_single_network.py
```

可用模型以脚本中的分支为准，包括 `unet`、`unet++`、`u2net`、`mcaunet`、`unet3p`、`uctransnet`、`udtransnet`、`attenunet`、`resunetpp`、`transunet` 和 `enet`。

## 评估

`test.py` 当前使用脚本内配置，而不是命令行参数。运行前需修改：

- `model_type`
- `checkpoints_path`
- 测试数据集路径

```bash
python test.py
```

脚本用于统计各病灶的 AUPR、Dice 等指标。

## 单张图像预测

`predict-3.py` 当前同样使用脚本内配置。请先设置：

- `model_type`
- `image_path`
- `model_path`
- `output_path`

```bash
python predict-3.py
```

仓库的 `input/` 与 `output/` 提供了少量输入及结果示例，但不包含运行所需的模型权重。

## 注意事项

- 训练、测试和预测脚本仍含原实验环境的 `/root/autodl-tmp/...` 绝对路径，复现实验前必须替换。
- 部分模型需要额外预训练权重，例如 TransUNet 的 ViT 权重。
- checkpoint 可能由 `DataParallel` 保存，加载时要注意参数名是否带 `module.` 前缀。
- 固定版本的 CUDA 包只适用于兼容的 NVIDIA 环境；CPU 或其他 CUDA 版本应使用 PyTorch 官方对应安装方式。
- 模型输出仅供科研和辅助分析使用。
