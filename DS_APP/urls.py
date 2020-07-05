'''
  @author Karan Dave  
'''

from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='HomePage'),
    path('search/',views.search,name='search'),
    path('result/',views.result,name='result'),
    path('sresult/',views.sresult,name='sresult'),
   
]
