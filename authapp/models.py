from django.db import models
from django.contrib.auth.models import User

class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=False)

    def __str__(self):
        return str(self.isActive)