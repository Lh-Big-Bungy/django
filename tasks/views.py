from django.shortcuts import render
from .models import Task

def task_list(request):
    # 从数据库获取Task对象列表
    tasks = Task.objects.all()
    # 指定渲染模板并向模板传递数据
    return render(request, "task/task_list.html", {"tasks": tasks})
