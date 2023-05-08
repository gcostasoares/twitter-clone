from django.db import models

class Tweet (models.Model):
    content = models.TextField(blank=True, null=True)
    image=models.FileField(upload_to='image/', blank=True, null=True)