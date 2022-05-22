from django.contrib import admin
from .models import autocomplete
# Register your models here.

@admin.register(autocomplete)
class autocompleteAdmin(admin.ModelAdmin):
    list_display=['first_name','middle_name','last_name']

# username admin pass admin