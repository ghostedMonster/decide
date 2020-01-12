import json
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.conf import settings
from django.http import Http404
from voting.models import Voting
from census.models import Census
from django.db.models import Count, Sum
from authentication.models import Voter
from store.models import Vote


from voting.models import Voting

from base import mods
from django.shortcuts import render

import requests
import json

class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            r1 = Voting.objects.filter(id=vid)[0]
            r2 = Vote.objects.filter(voting_id=vid).aggregate(num_votes=Count('voter_id'))
            
            context['voting'] = json.dumps(r[0])
            numero=[]

            vTotal=r2['num_votes']

            shareLink=""
            shareLink=genera_telegram(self.request, r1.name, r1.postproc, vid)
            print(2)
     
            for opt in r1.postproc:
                nv=(opt['votes']/r2['num_votes'])*100
                numero.append(nv)

            
            context['numero'] = numero
            ##Sacar el objeto census de la votacion y su voter id, habria que hacer un for con los [i]
            #Census.objects.filter(voting_id=1)[0].voter_id

            ##Participacion del censo
            nc=0.0
            edad={}
            estudios={}
            region={}
            profesion={}
            sexo={}

            for u in Census.objects.filter(voting_id=r1.id):

                nc=nc+1.0
                votante1=Voter.objects.filter(Usuario_id=u.voter_id)[0]
                e1=votante1.edad
                e1=str(e1)
        
                if(edad.get(e1) is not None):
                    edad[e1]=str(int(edad.get(e1)) + 1)
                else:
                    edad[e1]=str(1)

                try: 
                    estudios1=votante1.estudios
                    profesion1=votante1.profesion
                    region1=votante1.region
                    sexo1=votante1.sexo

                except:
                    print("Something went wrong")

                if(estudios.get(estudios1) is not None):
                    estudios[estudios1]=str(int(estudios.get(estudios1)) + 1)
                else:
                    estudios[estudios1]=str(1)

                if(profesion.get(profesion1) is not None):
                    profesion[profesion1]=str(int(profesion.get(profesion1)) + 1)
                else:
                    profesion[profesion1]=str(1)

                if(region.get(region1) is not None):
                    region[region1]=str(int(region.get(region1)) + 1)
                else:
                    region[region1]=str(1)
                
                if(sexo.get(sexo1) is not None):
                    sexo[sexo1]=str(int(sexo.get(sexo1)) + 1)
                else:
                    sexo[sexo1]=str(1)                

            nc=vTotal/nc

            context['pC'] = str(nc*100.0)
            context['edad'] = edad
            context['profesion'] = profesion
            context['region'] = region
            context['estudios'] = estudios
            context['sexo'] = sexo

            context['shareLink'] = shareLink
      
            ##Sacar el user a partir del voter id 
            #User.objects.filter(id=1)[0].username
  
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
    
class VotingListView(ListView):
    model = Voting
    context_object_name = 'voting_list'  
    queryset = Voting.objects.all()
    template_name = 'visualizer/voting_list.html'  


class VotingDetailView(DetailView):
    model = Voting
    template_name = 'visualizer/voting_detail.html'
    def voting_detail_view(request,pk):
        try:
            voting_id=Voting.objects.get(pk=pk)
        except Voting.DoesNotExist:
            raise Http404("Voting does not exist")

        #voting_id=get_object_or_404(Voting, pk=pk)
        
      
def genera_telegram(request, votingName, opciones, vid):
        token='d180fa8b90d4eebace7489dccf91fd5df2cec4ab21b93ab99038267a4c7d'
        api_url_base='https://api.telegra.ph/'
        texto="Los resultados de la encuesta " + votingName + ", son los sigientes: " + "\n"

        for o in opciones:
            texto=texto + str(o['option']) +": " + str(o['votes']) + " voto/s. " + "\n"

        url_decide = request.build_absolute_uri()

        texto=texto + 'Visita ' + '"' +',{"tag":"a","attrs":{"href":"' + url_decide + '"},"children":["' + url_decide + '"]},"' + ' para mas información.'
        contenido='[{"tag":"p","children":[' + '"' + texto + '"' + ']}]'
        print(contenido)

        url_create = api_url_base + 'createPage?access_token=' + token + '&title=' + str(votingName) + '&author_name=Decide&content=' +  contenido + '&return_content=true'
        
        print(url_create)

        response=requests.get(url_create)
        shareLink=""

        if response.status_code==200:
            respuesta=json.loads(response.text)
            respuesta=respuesta["result"]
            print(respuesta)

            post=respuesta["url"]

            print(post)
            shareLink='https://telegram.me/share/url?url=' + post +'&text=' + 'Quería compartir contigo los resultados de esta votación:'

        return shareLink
