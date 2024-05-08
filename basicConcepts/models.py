# from django.db import models

# # Create your models here.
# class image_model(models.Model):
# 	title = models.CharField(max_length = 200)
# 	img = models.ImageField(upload_to = "images/")

# 	def __str__(self):
# 		return self.title
        
from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
