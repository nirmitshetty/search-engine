
from django.contrib import admin
from django.urls import path

from QuerySearch import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',views.home, name="home"),
    #path('process_search/',views.gen_search_json, name="process_search"),
    path('querySearch/<str:query>/<int:option>',views.querySearch,name='querySearch'),
]
