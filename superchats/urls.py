from django.urls import path 
from .views import superchats_view 
 
urlpatterns = [  
    path('superchats/', superchats_view, name='superchats'),
]