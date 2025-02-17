from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView, name='home'),  
    path('get-municipalities/<int:district_id>/', get_municipalities, name='get_municipalities'),
    path('location/', LocationView, name='location'), 
    path('flooring/', Flooring, name='flooring'),  
    path('other/', Other, name='other'),  
    path('summary/', Summary, name='summary'),  
    path('calculation/cost/', CostCalculation, name='cost_calculation'),  

]
