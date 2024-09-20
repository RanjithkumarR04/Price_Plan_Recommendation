from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('additional_details/', views.additional_details, name='additional_details'),
    path('output/', views.output, name='output'),
]
