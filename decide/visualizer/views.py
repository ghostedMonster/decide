import json
from django.http import HttpResponse
from reportlab.pdfgen import canvas

from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods
from django.shortcuts import render
from reportlab.lib.utils import ImageReader

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
        
        ## Creamos el objeto HttpResponse con las apropiadas cabeceras PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="datos_decide.pdf"'

        logo = ImageReader('https://images.squarespace-cdn.com/content/v1/531365fbe4b060dc36b4afa6/1553794264094-CFUAKKDDNYRG14W2CIXU/ke17ZwdGBToddI8pDm48kHhlTY0to_qtyxq77jLiHTtZw-zPPgdn4jUwVcJE1ZvWhcwhEtWJXoshNdA9f1qD7Xj1nVWs2aaTtWBneO2WM-sIRozzR0FWTsIsFVspibqsB7eL2qd43SOgdOvkAOY75w/django.png?format=300w')
        ## Creamos el objeto PDF 
        p = canvas.Canvas(response)
        #A partir de aquí se introducen los elementos que se imprimirán en PDF

        ## Dibujamos la imagen plantilla que irá en la cabecera 
        p.drawImage(logo, -20, 600, mask='auto')
        
        #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica.
        p.setFont("Helvetica", 16)
        #Dibujamos una cadena en la ubicación X,Y especificada.
        p.drawString(230, 790, u"PLATAFORMA DECIDE")
        p.setFont("Helvetica", 14)
        p.drawString(200, 770, u"REPORTE DE DATOS DE VOTANTES")
        p.setFont("Helvetica", 10)
        p.drawString(275, 680, u"Porcentaje 1: 0.25")
        p.setFont("Helvetica", 10)
        p.drawString(275, 650, u"Porcentaje 2: 0.75")
        p.setFont("Helvetica", 10)
        p.drawString(275, 620, u"Votos: 1357")
        p.setFont("Helvetica", 10)
        p.drawString(275, 590, u"Votantes: 1521")
        p.setFont("Helvetica", 10)
        p.drawString(275, 560, u"Desviación: 0.321457")

        ## Cerramos el objeto PDF.
        p.showPage()
        p.save()
        return response              
         
    
    