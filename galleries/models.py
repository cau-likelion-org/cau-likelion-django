from django.db import models

# Create your models here.
class test(models.Model):
    testfield = models.CharField(max_length=200)
    photo = models.FileField()
    def __str__(self):
        return self.testfield