import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods
from django.shortcuts import render

class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        return context
    
    def hola_mundo(request):
        return render(request, 'visualizer/hola_mundo.html')

    def bypass(request):
        porcentajes  = [0.25, 0.75]
        votos = 1357
        votantes = 1521
        desviacion = 0.321457
        return render(request, 'visualizer/visualizador.html', {'porcentajes': porcentajes, 'votos': votos, 'votantes':votantes, 'desviacion':desviacion})