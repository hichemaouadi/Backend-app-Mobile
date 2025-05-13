from django.db import models
from django.contrib.auth.models import User

class SuperAdmin(models.Model) : 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='superadmin')
    email = models.CharField(max_length=200,null = False)
    is_blocked = models.BooleanField(default = False , editable=False)
class Admin(models.Model) : 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin')
    email = models.CharField(max_length=200,null = False)
    is_blocked = models.BooleanField(default = False)
class Utilisateur(models.Model) : 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    email = models.CharField(max_length=200,null = False)
    is_blocked = models.BooleanField(default = False)
