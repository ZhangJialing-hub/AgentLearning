
import json


def validate_plan_format(plan):

    if not isinstance(plan, dict):
        return False, "计划必须是 JSON 对象"

    if "goal" not in plan:
        return False, "缺少 goal 字段"

    if "plan" not in plan:
        return False, "缺少 plan 字段"

    if not isinstance(plan["plan"], list):
        return False, "plan 必须是列表"

    for item in plan["plan"]:

        if not isinstance(item, dict):
            return False, "每天的计划必须是对象"

        if "day" not in item:
            return False, "计划缺少 day 字段"

        if "task" not in item:
            return False, "计划缺少 task 字段"

        if "hours" not in item:
            return False, "计划缺少 hours 字段"

        if isinstance(item["hours"], bool) or not isinstance(item["hours"], (int, float)):
            return False, f"{item['day']}的学习时长必须是数字"

        if item["hours"] <= 0:
            return False, f"{item['day']}的学习时长必须大于0"

    return True, "格式正确"


# 模拟大模型返回的 JSON 字符串
content = """
{
    "goal":"学习c++",
    "plan": [
        {
            "day": "第1天",
            "task": "复习指针",
            "hours": "2个小时"
        }
    ]
}
"""

# 第一步：尝试解析 JSON
try:

    plan = json.loads(content)

    # 第二步：检查数据结构
    is_valid, message = validate_plan_format(plan)

    if is_valid:
        print("计划格式检查通过！")
    else:
        print("计划格式检查失败：", message)

except json.JSONDecodeError:
    print("模型返回的内容不是合法 JSON")
