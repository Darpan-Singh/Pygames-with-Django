from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('g1',views.g1,name='g1'),
    path('g3',views.g3,name='g3'),
    path('g4',views.g4,name='g4'), 
    path('g5',views.g5,name='g5'), 
]