from django.db import models


class ImageUpload(models.Model):
    image = models.ImageField(upload_to='images/')
    text_watermark = models.CharField(max_length=200)
    font = models.IntegerField()   
    uploaded_at = models.DateTimeField(auto_now_add=True)