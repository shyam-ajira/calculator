from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView, name='home'),  
    path('get-municipalities/<int:district_id>/', get_municipalities, name='get_municipalities'),
    path('location/', LocationView, name='location'), 
    path('flooring/', FlooringView, name='flooring'),  
    path('room/', RoomView, name='room'),  
    path('other/', OtherView, name='other'),  
    path('summary/', Summary, name='summary'),  
    path('calculation/cost/', CostCalculation, name='cost_calculation'),  

]
