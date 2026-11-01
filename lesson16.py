
import json

plan = {
    "goal": "复习C++",
    "plan": [
        {
            "day": "第1天",
            "task": "复习指针",
            "hours": 2
        },
        {
            "day": "第2天",
            "task": "复习引用",
            "hours": 1.5
        }
    ]
}

# 保存计划
with open("study_plan.json", "w", encoding="utf-8") as f:
    json.dump(plan, f, ensure_ascii=False, indent=4)

print("计划保存成功！")
