from django.urls import path
from .views import VisualizerView
from .views import VotingListView
from .views import VotingDetailView


urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view(), name="Predeterminada"),
    path('hola_mundo/', VisualizerView.hola_mundo),
    path('bypass/', VisualizerView.bypass),
<<<<<<< HEAD
    path('descargaPDF/', VisualizerView.descargaPDF),
        
=======
    path('votings/', VotingListView.as_view(), name='votings'),
    path('voting/<int:pk>/', VotingDetailView.as_view(), name='voting-detail'),


>>>>>>> develop
]
