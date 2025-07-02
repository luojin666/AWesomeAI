# NLP层后端接口说明

---

## 1. 启动后端

```bash
python main.py
```
默认监听端口：`5000`

---

## 2. 前端接口说明

### 2.1 上传无人机信息

- **接口地址**：`POST /drones`
- **请求体**：无人机信息列表（JSON数组），每个元素包含：`编号`（int）、`状态`（str）、`电量`（int）
- **示例**：

```json
[
  {"编号": 1, "状态": "空闲", "电量": 90},
  {"编号": 2, "状态": "作业中", "电量": 60},
  {"编号": 3, "状态": "空闲", "电量": 85}
]
```

- **返回**：
```json
{"msg": "无人机信息已更新", "count": 3}
```

- **前端调用示例**：
```js
fetch('http://localhost:5000/drones', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify([
    {编号: 1, 状态: '空闲', 电量: 90},
    {编号: 2, 状态: '作业中', 电量: 60}
  ])
})
.then(res => res.json())
.then(data => {
  // data.msg === "无人机信息已更新"
});
```

---

### 2.2 对话：发送消息

- **接口地址**：`POST /chat`
- **请求体**：
```json
{"message": "你的用户输入内容"}
```
- **返回**：
  - `reply`：AI助手回复内容（字符串）
  - `task`：如果已分配任务，返回任务表（JSON对象）
  - `error`：如有错误或无人机不可用，返回错误信息

- **前端调用示例**：
```js
fetch('http://localhost:5000/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({message: '请帮我安排明天7点在A地巡检'})
})
.then(res => res.json())
.then(data => {
  // data.reply 显示到对话框
  // data.task 存在时，显示任务表
  // data.error 存在时，显示错误信息
});
```

- **返回示例**：
```json
{
  "reply": "任务：巡检，时间：07:00，地点：A。已为您分配无人机编号4。",
  "task": {
    "任务": "巡检",
    "时间": "07:00",
    "地点": "A",
    "无人机编号": 4
  }
}
```

---

### 2.3 获取最新任务表

- **接口地址**：`GET /task`
- **返回**：最新分配的任务表（JSON对象）
- **前端调用示例**：
```js
fetch('http://localhost:5000/task')
  .then(res => res.json())
  .then(task => {
    // 显示任务表内容
  });
```
- **返回示例**：
```json
{
  "任务": "巡检",
  "时间": "07:00",
  "地点": "A",
  "无人机编号": 4
}
```

---

## 3. 交互流程建议

1. 前端页面加载时，先通过 `/drones` 上传当前所有无人机状态。
2. 用户在对话框输入内容，前端通过 `/chat` 发送消息，显示 AI 回复。
3. 若 AI 回复中包含任务表（`task` 字段），可直接展示任务分配结果。
4. 也可通过 `/task` 随时获取最新任务表。

---

如有更多需求或问题，请联系后端开发者。
