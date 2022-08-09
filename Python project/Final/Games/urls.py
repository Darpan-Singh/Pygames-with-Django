from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('g1',views.g1,name='g1'),
    path('g2',views.g2,name='g2')    
]