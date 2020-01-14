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
#para añadir la pagina index.html
from django.shortcuts import render



def home_view(request):
    return render(
        request,
        'home.html',
    )

class StoreView(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('voting_id', 'voter_id', 'voter_time','voter_sex','voter_age','voter_ip')
    #filter_fields = ('voting_id', 'voter_id')


    def get(self, request):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        return super().get(request)

    def post(self, request):
        """
         * voting: id
         * voter: id
         * vote: { "a": int, "b": int }
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

        """
        g = GeoIP()
        ip = request.data.get('ip', None)
        if ip:
            city = g.city(ip)['city']
        else:
            city = 'Sevilla' # default """


        a = vote.get("a")
        b = vote.get("b")

        utime = vote.get("voted")
     
        defs = { "a": a, "b": b }
        
        utime = vote.get("voted")

        usex = vote.get("voter_sex")
    
        if usex is not  'Hombre' or 'Mujer':
            return Response({}, status=status.HTTP_400_BAD_REQUEST) 

        uage = vote.get("voter_age")

        if uage < 18:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        uip = vote.get("voter_ip")
        ucity = vote.get("voter_city")

        defs = { "a": a, "b": b }
        v, _ = Vote.objects.get_or_create(voting_id=vid, voter_id=uid,voter_time=utime,voter_sex=usex,voter_age=uage,voter_ip=uip,voter_city=ucity,
             defaults=defs)
        #v, _ = Vote.objects.get_or_create(voting_id=vid, voter_id=uid,
         #                                 defaults=defs)
        v.a = a
        v.b = b
        v.voted = utime
        v.voter_age = uage
        v.voter_sex = usex
        v.voter_ip = uip
        v.voter_city = ucity

        v.save()
        
        return  Response({})     

      