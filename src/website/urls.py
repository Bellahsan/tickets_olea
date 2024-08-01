from django.urls import path
from .views import *


urlpatterns = [
    path('index/', index, name='index'),
    path('tickets/', TicketsView.as_view(), name='tickets'),
    path('users/', UsersView.as_view(), name='users'),
    path('types/', TypesTicketsView.as_view(), name='types'),
]