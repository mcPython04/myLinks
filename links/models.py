from django.db import models

# Create your models here.
class link(models.Model):
    hyperlink = models.CharField(max_length=200, default = '')
    website_name = models.CharField(max_length=200, default= '')
    image = models.ImageField(upload_to='images/', blank=True)
    def __str__(self):
        return self.website_name
    def __hyperlink__(self):
        return self.hyperlink
