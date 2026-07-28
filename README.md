# DiabRetina AI

面向糖尿病视网膜病变（Diabetic Retinopathy, DR）的眼底图像病灶分割与辅助诊断平台。

项目包含病灶分割模型训练代码、Flask 推理服务和 React Web 前端，可识别并可视化以下四类病灶：

| 缩写 | 病灶 |
| --- | --- |
| MA | 微动脉瘤（Microaneurysm） |
| HE | 出血（Hemorrhage） |
| EX | 硬性渗出（Hard Exudate） |
| SE | 软性渗出（Soft Exudate） |

> [!IMPORTANT]
> 本项目用于课程研究、算法实验与辅助分析，不属于医疗器械，输出不能替代医生诊断或治疗建议。

## 项目组成

```text
Diabetic-Retinopathy/
├── train/                     # 数据加载、模型、损失函数、训练/测试/预测脚本
├── DiabRetina_AI_Backend/     # Flask 推理、AI 辅助分析和 PDF 报告服务
├── DiabRetina_AI_Frontend/    # React 用户界面
├── Report.pdf                 # 项目报告
└── README.md
```

各模块的详细配置见：

- [训练与评估说明](train/README.md)
- [后端说明](DiabRetina_AI_Backend/README.md)
- [前端说明](DiabRetina_AI_Frontend/README.md)
- [后端 API 参考](docs/API.md)

## 功能

- 眼底图像上传及预处理
- MA、HE、EX、SE 四类病灶的像素级分割
- 病灶区域叠加显示和连通区域计数
- 患者信息与诊断记录管理
- 调用大模型生成辅助诊断文字
- 生成和下载 PDF 诊断报告
- 多种分割网络的训练与对比

训练代码包含 UNet、UNet++、U2Net、MCA-UNet、UNet3+、UCTransNet、UDTransNet、Attention U-Net、ResUNet++、TransUNet 和 ENet 等模型实现。

## 快速开始

### 1. 获取代码和模型

```bash
git clone https://github.com/Euuugeo/Diabetic-Retinopathy.git
cd Diabetic-Retinopathy
```

从 [Hugging Face 模型仓库](https://huggingface.co/Euuugeo/DiabeticRetinopathy)下载后端所需权重，并放置为：

```text
DiabRetina_AI_Backend/model/model-mcaunet.pth.tar
```

`model/` 和权重文件未包含在本 GitHub 仓库中，缺少权重时后端无法启动。

### 2. 启动后端

建议使用 Python 3.8。PyTorch 版本及 CUDA 支持需要与本机环境匹配。

```bash
cd DiabRetina_AI_Backend
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

在该目录创建 `.env`：

```dotenv
VOLCENGINE_API_URL=https://your-api-endpoint.example.com
VOLCENGINE_API_KEY=your-api-key
```

安装文泉驿正黑字体后启动服务：

```bash
python main.py
```

默认监听 `http://0.0.0.0:8005`。Linux 生产环境也可执行 `./run.sh`。

### 3. 启动前端

```bash
cd DiabRetina_AI_Frontend
npm install
npm start
```

开发服务器默认打开 `http://localhost:3000`。

> [!NOTE]
> 当前前端请求地址和后端报告下载地址写在源码中，默认指向项目原部署服务器。进行本地开发时，请将前端 `src/layouts/diagnosis/index.js` 和 `src/layouts/history/index.js` 中的 API 地址改为 `http://localhost:8005`，并同步调整后端 `main.py` 中的报告下载基础地址。

## 技术栈

- 模型：PyTorch、TorchVision
- 图像处理：OpenCV、SimpleITK、Albumentations
- 后端：Flask、Gunicorn、ReportLab
- 前端：React 18、Material UI
- AI 辅助分析：兼容项目当前火山引擎接口配置

## 数据与训练

训练脚本支持 IDRiD 和 DDR 数据集，但数据集体积较大且受各自许可约束，因此未随仓库分发。下载数据后，需要根据本机路径修改 `train/DataSet.py` 及训练、测试脚本中的数据和权重路径。具体目录约定与已知限制见[训练说明](train/README.md)。

## 课程信息

同济大学计算机科学与技术学院，2025 年专业方向综合项目，第 7 组。

| 成员 | 分工 |
| --- | --- |
| 陈乐俊杰（2250944） | 实验设计、UNet 复现、模型训练与优化、AI Agent 大模型评估 |
| 林继燊（2250758） | 数据标准化与增强、前后端开发、AI Agent 构建 |
| 王成伟（2251941） | UNet 复现、模型训练与优化、检测结果可视化 |

## 许可

各子项目附有各自的 `LICENSE` 文件。使用数据集、预训练权重、第三方模型代码和前端模板时，还需遵守对应来源的许可条款。
