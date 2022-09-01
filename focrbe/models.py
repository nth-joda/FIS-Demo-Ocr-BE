from django.db import models

# Create your models here.


class Detection(models.Model):
    image = models.ImageField(upload_to='images/')
    type = models.TextField()
    result = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.result
