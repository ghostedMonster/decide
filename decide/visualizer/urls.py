from django.urls import path
from .views import VisualizerView


urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('hola_mundo/', VisualizerView.hola_mundo),
    path('bypass/', VisualizerView.bypass),
    path('descargaPDF/', VisualizerView.descargaPDF),
        
]
