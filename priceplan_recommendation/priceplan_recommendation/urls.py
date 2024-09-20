from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Path for entering the phone number
    path('additional-details/', views.additional_details, name='additional_details'),  # Path for entering additional details if phone number is not found
    path('output/', views.output, name='output'),  # Path for displaying the recommended plans
]
