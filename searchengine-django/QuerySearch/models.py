from django.db import models

# Create your models here.

class autocomplete(models.Model):
    
    first_name=models.CharField(max_length=30)
    middle_name=models.CharField(max_length=30,null=True,blank=True)
    last_name=models.CharField(max_length=30,null=True,blank=True)

class covid(models.Model):
 
    #index=models.CharField(max_length=30)
    question=models.CharField(max_length=30,null=True,blank=True)
    answer=models.CharField(max_length=30,null=True,blank=True)
    answer_html=models.CharField(max_length=30,null=True,blank=True)
    link=models.CharField(max_length=30,null=True,blank=True)
    name=models.CharField(max_length=30,null=True,blank=True)
    source=models.CharField(max_length=30,null=True,blank=True)
    category=models.CharField(max_length=30,null=True,blank=True)
    country=models.CharField(max_length=30,null=True,blank=True)
    region=models.CharField(max_length=30,null=True,blank=True)
    city=models.CharField(max_length=30,null=True,blank=True)
    lang=models.CharField(max_length=30,null=True,blank=True)
    last_update=models.CharField(max_length=30,null=True,blank=True)
    question_ar=models.CharField(max_length=30,null=True,blank=True)
    answer_ar=models.CharField(max_length=30,null=True,blank=True)

class video(models.Model):
    
    Youtube_link=models.CharField(max_length=50,null=True,blank=True)
    VID=models.CharField(max_length=30,null=True,blank=True)
    Question=models.CharField(max_length=30,null=True,blank=True)
    Transcript=models.CharField(max_length=30,null=True,blank=True)
    Description=models.CharField(max_length=500,null=True,blank=True)