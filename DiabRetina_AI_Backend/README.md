# DiabRetina AI 后端

基于 Flask 的推理与报告服务，负责眼底图像预处理、MCA-UNet 病灶分割、病灶计数、AI 辅助诊断和 PDF 报告生成。

## 运行要求

- 推荐 Python 3.8
- 推理权重 `model/model-mcaunet.pth.tar`
- 文泉驿正黑字体 `wqy-zenhei.ttc`
- 火山引擎大模型接口地址与密钥

当前代码固定从 Linux 路径 `/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc` 加载字体。在 Windows、macOS 或字体路径不同的 Linux 发行版上，需要修改 `main.py` 中的字体路径。

## 安装

```bash
cd DiabRetina_AI_Backend
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

从 [模型仓库](https://huggingface.co/Euuugeo/DiabeticRetinopathy)下载权重，目录应为：

```text
DiabRetina_AI_Backend/
├── model/
│   └── model-mcaunet.pth.tar
├── nets/
├── main.py
└── ...
```

## 环境变量

在后端目录创建 `.env`。不要提交真实密钥。

```dotenv
VOLCENGINE_API_URL=https://your-api-endpoint.example.com
VOLCENGINE_API_KEY=your-api-key
```

这两个变量在模块加载时即会校验，任一缺失都会导致服务启动失败。

## 启动

开发环境：

```bash
python main.py
```

Linux/Gunicorn：

```bash
chmod +x run.sh
./run.sh
```

服务默认监听 `0.0.0.0:8005`。`run.sh` 配置了 4 个 Gunicorn worker；每个 worker 都会分别加载模型，请根据显存或内存调整 worker 数量。

## 运行时目录

服务会自动创建以下目录：

- `original-image/`：用户上传的原图
- `preprocessed-image/`：模型输入对应的预处理图
- `predicted-image/`：病灶掩膜叠加图
- `diagnosis-record/`：用于历史列表的文本记录
- `diagnostic-report/`：生成的 PDF 报告

这些目录可能包含患者信息或医疗图像。真实部署时应配置访问控制、数据保留期限、加密和定期清理策略，不应将运行数据提交到 Git。

## API

主要端点：

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| `POST` | `/predict` | 上传眼底图像并返回分割结果与病灶数量 |
| `POST` | `/generate_diagnosis` | 调用大模型生成辅助诊断文字 |
| `POST` | `/generate_report` | 生成 PDF 报告和历史记录 |
| `GET` | `/diagnostic-report/<uuid>` | 获取 PDF 报告 |
| `GET` | `/history` | 获取历史记录 |

请求字段和响应示例见 [API 文档](../docs/API.md)。

## 部署注意事项

- `main.py` 中的报告 URL 当前固定为 `http://110.42.214.164:8005`，部署到其他地址时需要修改。
- CORS 当前对所有来源开放，生产环境应限制为可信前端域名。
- 上传大小当前无限制，生产环境应设置合理的 `MAX_CONTENT_LENGTH`。
- 服务没有身份认证，不能直接暴露在承载真实患者数据的公网环境。
- API 密钥只应保存在服务端环境变量中。
- PDF 生成依赖中文字体，缺少字体时服务无法正常启动或输出中文。
- 本服务的输出不构成医疗诊断。
