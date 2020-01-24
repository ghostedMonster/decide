from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.BackupView.as_view(), name='backup'),
]
