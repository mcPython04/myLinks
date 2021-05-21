from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class StaticLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True, unique=True)
    file = models.FileField(upload_to='static_links')
    description = models.TextField(blank=True)
    context = models.TextField()

    def __str__(self):
        return self.name
