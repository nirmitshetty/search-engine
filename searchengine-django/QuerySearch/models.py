from django.db import models

# Create your models here.

class autocomplete(models.Model):
    
    first_name=models.CharField(max_length=30)
    middle_name=models.CharField(max_length=30,null=True,blank=True)
    last_name=models.CharField(max_length=30,null=True,blank=True)


