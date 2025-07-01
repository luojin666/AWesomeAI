from openai import OpenAI
import re
import json

client = OpenAI(
    api_key="sk-f5d5c9ce3454470ea8dd9ac785202944",
    base_url="https://api.deepseek.com"
)

system_prompt = (
    "你是一个无人机管理软件的NLP助手。"
    "用户需要提供任务（巡检或播撒农药）、时间（24小时任意时间）、地点（已开通A、B、C、D、E五个地点）。"
    "如果信息不全，请追问用户直到获得所有信息。"
    "当信息齐全时，输出任务表，格式为：任务：xxx，时间：xxx，地点：xxx。"
    "如果用户问与无人机任务无关的问题，请回复：很抱歉，暂时不支持此功能。"
)

messages = [
    {"role": "system", "content": system_prompt},
]

while True:
    user_input = input("你：")
    if user_input.lower() in ["exit", "quit", "退出"]:
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=True
    )

    print("助手：", end="", flush=True)
    assistant_reply = ""
    for chunk in response:
        if chunk.choices[0].delta and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            assistant_reply += content
    print()  # 换行
    messages.append({"role": "assistant", "content": assistant_reply})

    # 调试输出
    print("DEBUG:", repr(assistant_reply))

    # 尝试从AI回复中提取任务表并输出为JSON
    match = re.search(r"任务[：:](.*?)[，,]\s*时间[：:](.*?)[，,]\s*地点[：:](.*?)(。|$)", assistant_reply)
    if match:
        task_json = {
            "任务": match.group(1).strip(),
            "时间": match.group(2).strip(),
            "地点": match.group(3).strip()
        }

        # 读取无人机状态
        drones = []
        with open("1.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("编号"):
                    continue
                parts = line.split(",")
                if len(parts) != 3:
                    continue
                drone_id = int(parts[0])
                status = parts[1]
                battery = int(parts[2])
                drones.append({"编号": drone_id, "状态": status, "电量": battery})

        # 筛选空闲且电量大于80%的无人机
        available = [d for d in drones if d["状态"] == "空闲" and d["电量"] > 80]

        if available:
            # 按电量降序，编号升序排序
            available.sort(key=lambda d: (-d["电量"], d["编号"]))
            selected = available[0]
            task_json["无人机编号"] = selected["编号"]
            print("任务表(JSON)：", json.dumps(task_json, ensure_ascii=False, indent=2))
            with open("task.json", "w", encoding="utf-8") as f:
                json.dump(task_json, f, ensure_ascii=False, indent=2)
            print(f"已分配无人机编号：{selected['编号']}，任务表已保存到 task.json")
        else:
            print("无可作业无人机，请继续等待。")
        break  # 检测到任务表后，终止对话