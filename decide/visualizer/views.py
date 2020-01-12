import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from voting.models import Voting
from census.models import Census
from django.db.models import Count, Sum
from authentication.models import Voter
from store.models import Vote


from base import mods


class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            r1 = Voting.objects.filter(id=vid)[0]
            r2 = Vote.objects.filter(voting_id=vid).aggregate(num_votes=Count('voter_id'))
            
            numero=[]

            vTotal=r2['num_votes']
     
            for opt in r1.postproc:
                nv=(opt['votes']/r2['num_votes'])*100
                numero.append(nv)

            
            context['numero'] = numero
            for i in range(0, len(numero)):
                r[0]['postproc'][i]['porcentaje'] = numero[i]
            opciones=[]
            for i in range(0, len(numero)):
                opciones.append(r[0]['postproc'][i]['option'])
            context['opciones'] = opciones
            context['voting'] = json.dumps(r[0])
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
                print(e1)
        
                if(edad.get(e1) is not None):
                    edad[e1]=str(int(edad.get(e1)) + 1)
                else:
                    edad[e1]=str(1)

                try: 
                    estudios1=votante1.estudios
                    profesion1=votante1.profesion
                    region1=votante1.region
                    sexo1 = votante1.sexo

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
            context['edadKeys'] = list(edad.keys())
            context['edadValues'] = list(edad.values())
            context['profesion'] = profesion
            context['region'] = region
            context['estudios'] = estudios
            context['sexo'] = sexo
            ##Sacar el user a partir del voter id 
            #User.objects.filter(id=1)[0].username
  
        except:
            raise Http404

        return context
