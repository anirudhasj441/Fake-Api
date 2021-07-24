from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserExtend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Client(models.Model):
    client_name = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.client_name)

class Project(models.Model):
    project_name = models.CharField(max_length=250, null=True)
    users = models.ManyToManyField(User)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(UserExtend, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.pk)