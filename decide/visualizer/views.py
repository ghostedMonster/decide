import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from voting.models import Voting
from census.models import Census
from django.db.models import Count
from authentication.models import Voter


from base import mods


class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            r1 = Voting.objects.filter(id=vid)[0]
            r2 = Voting.objects.filter(id=vid).aggregate(num_votes=Count('postproc'))
            context['voting'] = json.dumps(r[0])
            numero=[]

            vTotal=r2['num_votes']
            for opt in r1.postproc:
                nv=(opt['votes']/r2['num_votes'])*100
                numero.append(nv)

            
            context['numero'] = numero
            ##Sacar el objeto census de la votacion y su voter id, habria que hacer un for con los [i]
            #Census.objects.filter(voting_id=1)[0].voter_id

            ##Participacion del censo
            nc=0.0
            edad={}
            for u in Census.objects.filter(voting_id=r1.id):

                nc=nc+1.0
                e1=Voter.objects.filter(Usuario_id=u.voter_id)[0].edad
                e1=str(e1)
                print(e1)
        
                if(edad.get(e1) is not None):
                    edad[e1]=str(int(edad.get(e1)) + 1)
                else:
                    edad[e1]=str(1)

            nc=vTotal/nc

            context['pC'] = str(nc*100.0)
            context['edad'] = edad
            print(edad)
            ##Sacar el user a partir del voter id 
            #User.objects.filter(id=1)[0].username
  
        except:
            raise Http404

        return context
