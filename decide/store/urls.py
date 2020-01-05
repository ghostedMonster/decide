from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.StoreView.as_view(), name='store'),
    path('changevote/', views.ChangevoteView, name='change'),
    path('home/', views.home_view, name='home')
    
]
