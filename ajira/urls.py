from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView, name='home'),  
    path('get-municipalities/<int:district_id>/', get_municipalities, name='get_municipalities'),
    path('location/', LocationView, name='location'), 
    path('flooring/', FlooringView, name='flooring'),  
    path('other/', OtherView, name='other'),  
    path('summary/', SummaryView, name='summary'),  
    path('result/', ResultView, name='result'), 
    path('report/<int:user_id>/', report, name='report'),
]
