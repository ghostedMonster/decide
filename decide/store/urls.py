from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.StoreView.as_view(), name='store'),
    path('changevoteview/', views.ChangevoteView, name='change'),
    path('changevote/', views.Changevote, name='home')
    
]
