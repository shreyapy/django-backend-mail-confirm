from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    task = models.CharField(max_length=50)
    date_created = models.DateField()
    due_date = models.DateField()
    category = models.CharField(max_length=30)
    user = models.ForeignKey(User, default = None, on_delete = models.CASCADE)