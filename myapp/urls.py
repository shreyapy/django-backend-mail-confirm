from django.urls import path
from .views import fetchAllTodos, addTodo, deleteTodos, updateTodo, fetchTodo

urlpatterns = [
    path('', fetchAllTodos, name='fetch-all-todos'),
    path('add-todo', addTodo, name='add-todo'),
    path('delete-todos', deleteTodos, name='delete-todos'),
    path('update-todo/<int:id>', updateTodo, name='update-todo'),
    path('todo/<int:id>', fetchTodo, name="fetch-todo")
]