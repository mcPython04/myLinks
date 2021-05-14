from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse


class link(models.Model):
    hyperlink = models.URLField(blank=True)
    website_name = models.CharField(max_length = 200, default= '')
    image = models.ImageField(upload_to='images/links')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    default = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.website_name


class collection(models.Model):
    name = models.CharField(max_length = 200, default= '')
    links = models.ManyToManyField(link)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name


