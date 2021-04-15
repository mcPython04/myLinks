from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
# Create your models here.


class link(models.Model):
    hyperlink = models.URLField(blank=True)
    website_name = models.CharField(max_length = 200, default= '')
    image = models.ImageField(upload_to='images')
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.website_name