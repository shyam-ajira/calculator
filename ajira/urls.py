from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView, name='home'),  
    path('get-municipalities/<int:district_id>/', get_municipalities, name='get_municipalities'),
    path('location/', LocationView, name='location'), 
    path('flooring/', Flooring, name='flooring'),  
    path('others/', Other, name='other'),  
    path('calculation/', Calculation, name='calculation'),  
]
