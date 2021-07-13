from django.db import models


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='img', blank=False)
    name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return str(self.id)
