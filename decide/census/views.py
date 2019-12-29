
import sys
import json

from django.views.generic import FormView
from pyexpat.errors import messages

from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED as ST_201,
    HTTP_204_NO_CONTENT as ST_204,
    HTTP_401_UNAUTHORIZED as ST_401,
    HTTP_409_CONFLICT as ST_409
)
from django.conf import settings
from base.perms import UserIsStaff
from rest_framework.utils import json

from .forms import CensusForm
from .models import Census
import django_excel as excel

from base import mods



class CensusView(TemplateView):
    template_name = "census/census.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CensusView, self).get_context_data(**kwargs)

        context['check_user'] = False

        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                context['check_user'] = True

        context['message'] = 'Aqui estamos'
        datos = Census.objects.all()

        #users = []
        #votings = []

        #for dato in datos:
        #    votings.append(mods.get('voting', params={'id': dato.voting_id}))
           # users.append(mods.get('auth', params={'id': dato.voter_id}))


        #datos_usuarios = []
        #datos_votaciones = []
        #for i in votings:
        #    datos_votaciones.append(i[0]['name'])
        context['datos'] = datos

        #for i in range(0, len(datos_usuarios)):
        #    context['datos'].append({})
        #    context['datos'][i]['voting_id'] = datos_votaciones[i]
        #    context['datos'][i]['voter_id'] = datos[i]['voter_id']
        return context

    def exportarDatos(request, format_exp=None):
        export = []
        export.append(['votantes', 'votaciones'])

        census = Census.objects.all()

        for censo in census:
            export.append([censo.voter_id, censo.voting_id])
        sheet = excel.pe.Sheet(export)

        if format_exp == "csv":
            return excel.make_response(sheet, "csv", file_name="censo.csv")
        elif format_exp == "ods":
            return excel.make_response(sheet, "ods", file_name="censo.ods")
        elif format_exp == "xlsx":
            return excel.make_response(sheet, "xlsx", file_name="censo.xlsx")
        else:
            messages.error(request, 'Este formato {} no es valido'.format(format_exp))


class CensusLogin(FormView):
    template_name = 'census/login.html'
    form_class = CensusForm
    success_url = '/census/census/'


    #def post(self, request, *args, **kwargs):
        #context = self.get_context_data()


class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)

    def create(self, request, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter)
                census.save()
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})


class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        census = Census.objects.filter(voting_id=voting_id, voter_id__in=voters)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')