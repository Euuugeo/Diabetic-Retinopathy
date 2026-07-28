# 后端 API 参考

默认基础地址：`http://localhost:8005`

## `POST /predict`

以 `multipart/form-data` 上传眼底图像，字段名必须为 `file`。

```bash
curl -X POST http://localhost:8005/predict \
  -F "file=@fundus.jpg"
```

成功响应：

```json
{
  "uuid": "a-generated-uuid",
  "preprocessed_image": "<base64-jpeg>",
  "predicted_image": "<base64-jpeg>",
  "lesion_counts": {
    "EX": 0,
    "HE": 0,
    "MA": 0,
    "SE": 0
  }
}
```

返回的两张图片是无 Data URL 前缀的 Base64 JPEG 字符串。前端显示时需要添加 `data:image/jpeg;base64,`。

## `POST /generate_diagnosis`

请求头为 `Content-Type: application/json`。所有下列字段均为必填：

```json
{
  "name": "示例患者",
  "gender": "女",
  "age": "50",
  "occupation": "教师",
  "contact": "已脱敏",
  "address": "已脱敏",
  "chief_complaint": "示例主诉",
  "present_illness": "示例现病史",
  "past_history": "示例既往史",
  "ma_count": 3,
  "he_count": 1,
  "ex_count": 2,
  "se_count": 0,
  "ma_severity": "1",
  "he_severity": "1",
  "ex_severity": "1",
  "se_severity": "0",
  "clinical_diagnosis": "仅作示例",
  "treatment_plan": "请由专业医生制定"
}
```

成功响应：

```json
{
  "ai_response": "辅助诊断文字"
}
```

严重程度编码为 `0` 至 `4`，分别对应健康、轻度 NPDR、中度 NPDR、重度 NPDR 和 PDR。

## `POST /generate_report`

请求体包含 `/generate_diagnosis` 的全部字段，并额外要求：

```json
{
  "uuid": "/predict 返回的 uuid",
  "ai_diagnosis": "辅助诊断文字"
}
```

服务使用对应 UUID 的预处理图和预测图生成 PDF。应先成功调用 `/predict`，再调用此接口。

成功响应：

```json
{
  "report_path": "http://host:8005/diagnostic-report/<uuid>"
}
```

## `GET /diagnostic-report/<uuid>`

返回 `application/pdf`。对应报告不存在时返回 `404`：

```json
{
  "error": "Diagnostic report not found"
}
```

## `GET /history`

返回按时间倒序排列的诊断记录：

```json
{
  "history": [
    {
      "uuid": "record-uuid",
      "name": "示例患者",
      "gender": "女",
      "age": "50",
      "occupation": "教师",
      "contact": "已脱敏",
      "address": "已脱敏",
      "time": "2025-01-01 12:00:00"
    }
  ]
}
```

## 错误处理

参数缺失通常返回 `400`，未捕获的处理错误返回 `500`，格式为：

```json
{
  "error": "错误说明"
}
```

接口当前没有认证、速率限制或患者数据隔离机制，仅适合受控的开发和演示环境。
