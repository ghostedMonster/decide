from django.urls import path
from . import views


urlpatterns = [

    path('census/', views.CensusView.as_view(), name='index'),
    path('', views.CensusLogin.as_view(), name='census_login'),
    path('resultados/<str:format_exp>', views.CensusView.exportarDatos, name='resultados'),
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),

]
