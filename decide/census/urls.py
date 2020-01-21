from django.urls import path, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [

    path('census/', views.CensusView.as_view(), name='index'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('create/', views.CensusNew.as_view(), name='new'),
    path('resultados/<str:format_exp>', views.CensusView.exportarDatos, name='resultados'),
    path('delete/<str:format_exp>', views.CensusView.eliminaDatos, name='delete'),

    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),

]
