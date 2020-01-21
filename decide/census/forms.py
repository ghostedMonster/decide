from django import forms


class CensusForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=100)


class CreateCensusForm(forms.Form):
    votante = forms.CharField(label='votante', max_length=100)
    votacion = forms.CharField(label='votacion', max_length=100)
