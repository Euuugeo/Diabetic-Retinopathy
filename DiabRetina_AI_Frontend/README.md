# DiabRetina AI 前端

基于 React 18 和 Material UI 的糖尿病视网膜病变辅助诊断界面，提供登录/注册界面、图像诊断、历史记录、健康科普和 AI Agent 页面。

## 环境要求

- Node.js 16 或 18
- npm
- 已启动的 DiabRetina AI 后端服务

## 安装与启动

```bash
cd DiabRetina_AI_Frontend
npm install
npm start
```

默认访问 `http://localhost:3000`。

常用命令：

```bash
npm start       # 开发服务器
npm run build   # 生产构建
npm test        # 测试
```

## 后端地址

当前诊断和历史页面在 `src/layouts/diagnosis/index.js`、`src/layouts/history/index.js` 中直接使用：

```text
http://110.42.214.164:8005
```

本地联调时，需要将诊断页面中的 `/predict`、`/generate_diagnosis`、`/generate_report` 以及历史页面中的 `/history` 地址改为：

```text
http://localhost:8005
```

后端必须同步允许前端来源访问。当前后端已启用全局 CORS，正式部署时建议限制允许的域名。

## 目录说明

```text
DiabRetina_AI_Frontend/
├── public/              # HTML 模板、图标和 Web App Manifest
├── src/
│   ├── assets/          # 图片与主题配置
│   ├── components/      # 通用 UI 组件
│   ├── context/         # 全局界面状态
│   ├── layouts/         # 登录、诊断、历史、科普和 Agent 页面
│   ├── App.js
│   ├── index.js
│   └── routes.js
├── package.json
└── package-lock.json
```

## 页面与路由

实际路由以 `src/routes.js` 为准。核心业务页面包括：

- 诊断：上传眼底图像、展示预处理图和病灶叠加结果、填写诊断信息并生成报告
- 历史：读取既往诊断记录
- 科普：糖尿病视网膜病变相关信息
- Agent：嵌入外部 AI Agent 页面

## 已知限制

- API 地址尚未通过环境变量配置，切换环境需要修改源码。
- 登录和注册页面主要用于界面演示，项目内未提供完整的账号认证后端。
- Agent 页面依赖外部网页，能否访问受网络与对方服务状态影响。
- 本项目用于教学与研究，不能替代专业医疗诊断。

## 致谢与许可

界面基于 Material Dashboard React 风格组件开发，第三方组件版权说明保留在源码文件中。项目许可见本目录的 `LICENSE`。
