import json
from django.http import HttpResponse
from reportlab.pdfgen import canvas

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

    def descargaPDF(request):
        
        ## Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="datos_decide.pdf"'

        ## Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)

        ## Draw things on the PDF. Here's where the PDF generation happens.
        ## See the ReportLab documentation for the full list of functionality.
        #p.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)
        
        #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        p.setFont("Helvetica", 16)
        #Dibujamos una cadena en la ubicación X,Y especificada
        p.drawString(230, 790, u"PLATAFORMA DECIDE")
        p.setFont("Helvetica", 14)
        p.drawString(200, 770, u"REPORTE DE DATOS DE VOTANTES")
        p.setFont("Helvetica", 10)
        p.drawString(100, 720, u"Porcentaje 1: 0.25")
        p.setFont("Helvetica", 10)
        p.drawString(100, 690, u"Porcentaje 2: 0.75")
        p.setFont("Helvetica", 10)
        p.drawString(100, 660, u"Votos: 1357")
        p.setFont("Helvetica", 10)
        p.drawString(100, 630, u"Votantes: 1521")
        p.setFont("Helvetica", 10)
        p.drawString(100, 600, u"Desviación: 0.321457")

        ## Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        return response              
         
    
    