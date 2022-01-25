from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"
        
class Queries(models.Model):
    queryid = models.AutoField(primary_key = True)
    query_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="query_users")
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(validators=[MinValueValidator(0)], default=0) # '0' : Open Query,   '1' : Resolved Query
    
    def __str__(self):
        return f"{self.queryid}"
