
def check_plan(plan, max_hours):
    errors = []

    for item in plan:
        if item["hours"] > max_hours:
            errors.append(
                f"{item['day']}安排超时：{item['hours']}小时，最多允许{max_hours}小时"
            )

    if errors:
        return False, errors

    return True, []


# 模拟大模型生成的计划
plan = [
    {"day": "第1天", "task": "复习第一章", "hours": 2},
    {"day": "第2天", "task": "复习第二章", "hours": 3},
    {"day": "第3天", "task": "复习第三章", "hours": 2.5}
]

# 调用验证函数
is_valid, errors = check_plan(plan, 2)

if is_valid:
    print("计划验证通过！")
else:
    print("计划验证失败！")
    for error in errors:
        print(error)
