from django.urls import path
from .views import VisualizerView
from .views import VotingListView

urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('hola_mundo/', VisualizerView.hola_mundo),
    path('bypass/', VisualizerView.bypass),
    path('votings/', VotingListView.as_view(), name='votings'),
    

]
