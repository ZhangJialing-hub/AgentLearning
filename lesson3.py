try:
    hours=int(input("请输入学习小时数"))
    print("学习小时数：",hours)
except ValueError:
    print("输入不合法")