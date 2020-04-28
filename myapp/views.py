from django.http import JsonResponse
from .models import Todo
from .forms import TodoForm
from .serializers import TodoSerializer
from rest_framework.decorators import api_view
from django.core.paginator import Paginator

@api_view(['GET'])
def fetchAllTodos(req):
    pageNo = req.GET['pageNo']
    objs = list(Todo.objects.filter(user=req.user))
    # objs.sort(key=lambda x: x.category, reverse=True)
    todos = []
    for obj in objs:
        todos.append(TodoSerializer(obj).data)
    p = Paginator(todos, 2)
    return JsonResponse(p.page(pageNo).object_list, safe=False)

@api_view(['GET'])
def fetchTodo(req, id):
    try:
        todo = Todo.objects.get(id=id)
        return JsonResponse(TodoSerializer(todo).data)
    except:
        return JsonResponse({'msg' : 'No data found'})

@api_view(['POST'])
def addTodo(req):
    if(req.method == "POST"):
        form = TodoForm(req.POST)
        print(form.is_valid())
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = req.user
            instance.save()
            return JsonResponse({'msg' : 'Submission succeeded'})
        return JsonResponse({'msg' : 'Submission failed'})

@api_view(['POST'])
def deleteTodos(req):
    if(req.method == "POST"):
        ids = req.POST.get('list', False)

        if not ids:
            return JsonResponse({'msg' : 'ID is not provided'})
        
        ids = ids.split(',')
        db = list(Todo.objects.values_list('id', flat=True))
        count = 0
        try:
            for id in ids:
                if int(id) in db:
                    todo = Todo.objects.get(id=id)
                    todo.delete()
                    count += 1
            return JsonResponse({'msg' : f'{count} item(s) deleted'})
        except:
            return JsonResponse({'msg' : 'Deletion Failed'})

@api_view(['POST'])
def updateTodo(req, id):
    try:
        if(req.method == "POST"):
            todo = Todo.objects.get(id=id)
            form = TodoForm(req.POST, instance = todo)  
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = req.user
                instance.save()
                return JsonResponse({'msg' : 'Updation succeeded'})
        return JsonResponse({'msg' : 'All fields are required'})
    except:
        return JsonResponse({'msg' : 'Updation failed'})
