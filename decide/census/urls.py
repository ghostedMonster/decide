from django.urls import path, include
from . import views


urlpatterns = [
    path('hola/', views.CensusView.as_view),
    #path('', views.CensusCreate.as_view(), name='census_create'),
    #path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
]
