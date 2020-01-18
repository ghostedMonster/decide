from django.utils import timezone
from django.utils.dateparse import parse_datetime
import django_filters.rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

from .models import Vote
from .serializers import VoteSerializer
from base import mods
from base.perms import UserIsStaff

import psycopg2
from django.http import HttpResponse
from django.shortcuts import render


class StoreView(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('voting_id', 'voter_id')

    def get(self, request):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        return super().get(request)

    def post(self, request):
        """
         * voting: id
         * voter: id
         * vote: { "a": int, "b": int }
         * change: int
        """

        vid = request.data.get('voting')
        voting = mods.get('voting', params={'id': vid})
        if not voting or not isinstance(voting, list):
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        start_date = voting[0].get('start_date', None)
        end_date = voting[0].get('end_date', None)
        not_started = not start_date or timezone.now() < parse_datetime(start_date)
        is_closed = end_date and parse_datetime(end_date) < timezone.now()
        if not_started or is_closed:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        uid = request.data.get('voter')
        vote = request.data.get('vote')
        

        if not vid or not uid or not vote:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        # validating voter
        token = request.auth.key
        voter = mods.post('authentication', entry_point='/getuser/', json={'token': token})
        voter_id = voter.get('id', None)
        if not voter_id or voter_id != uid:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        # the user is in the census
        perms = mods.get('census/{}'.format(vid), params={'voter_id': uid}, response=True)
        if perms.status_code == 401:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        changeV = request.data.get('change')

        if changeV != 41:
            # the user is reedinting the vote
            # crear una lista con los ids existentes en la votacions
            con = psycopg2.connect(
                host = '127.0.0.1',
                database = 'postgres',
                user = 'decide',
                password = 'decide'
            )
            # create cursor
            cur = con.cursor()
            uid = request.data.get('voter') # cojer el id del votante
            #uid = int(uid)

            cur.execute("SELECT voter_id FROM store_vote WHERE voter_id = %s;", (uid,))
            
            row = cur.fetchone()

            # close conection
            con.close()
            
            # Comprovar si el votante ha votado ya, si es que si, no deja (service unvailable)
            if row is not None:
                return Response({}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
 
        a = vote.get("a")
        b = vote.get("b")

        defs = { "a": a, "b": b }
        v, _ = Vote.objects.get_or_create(voting_id=vid, voter_id=uid,
                                          defaults=defs)
        
        v.a = a
        v.b = b

        v.save()

        if changeV == 41:
            return Response({}, status= status.HTTP_501_NOT_IMPLEMENTED)
            
        return  Response({})

# Printea por pantalla Hellow
def ChangevoteView(request):
    return HttpResponse("<h1>Hellow!<h1>")
    '''return render (
        request,
        'base.html',
    )'''

# Redirige a la pagina home.html
def Changevote (request, *args, **kwargs):
    
    con = psycopg2.connect(
            host = '127.0.0.1',
            database = 'postgres',
            user = 'decide',
            password = 'decide'
        )
    # create cursor
    cur = con.cursor()
    uid = 3 #request.data.get('voter') # cojer el id del votante
    #uid = int(uid)

    cur.execute("SELECT voting_id FROM store_vote WHERE voter_id = %s;", (uid,))

    row = cur.fetchone()

    id_votacion = row
    #name_votacion = 
    context= {
        'id': id_votacion,
        'id2': 'Hola',
        'request': request,
        #'nombre': name_votacion,
        }

    # En context pasamos las votaciones en las que ha participado (ID y nombre votación)
    return render(request, "home.html", context)
     



