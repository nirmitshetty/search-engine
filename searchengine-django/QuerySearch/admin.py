from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(autocomplete)
class autocompleteAdmin(admin.ModelAdmin):
    list_display=['first_name','middle_name','last_name']

@admin.register(covid)
class covidAdmin(admin.ModelAdmin):
    list_display=['question','answer','answer_html','link','name','source','category']

@admin.register(video)
class videoAdmin(admin.ModelAdmin):
    list_display=['Youtube_link','VID','Question','Transcript']

# username admin pass admin