'''
tasks=["完成练习","整理笔记","准备面试"]

print(tasks[0])
print(tasks[1])
print(tasks[2])
tasks.append("新任务")
print(tasks[-1])
print(len(tasks))
'''
def cal(tasks):
    total=0
    for task in tasks:
        total=total+task["hours"]
    return total
tasks=[
    {"name":"整理笔记","hours":2},
     {"name":"准备面试","hours":3},
      {"name":"完成练习","hours":1}
    ]
for task in tasks:
    print(task["name"],"耗费",task["hours"])
result=cal(tasks)
print("总耗时",result,"小时")