from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
REGION_CHOICES = [('Galicia','Galicia'), ('Principado de Asturias','Principado de Asturias'), 
                  ('Cantabria','Cantabria'), ('País Vasco','Pais Vasco'), 
                  ('Navarra','Navarra'), ('Aragon','Aragón'), 
                  ('Catalunya','Cataluña'), ('Castilla y Leon','Castilla y León'), 
                  ('La Rioja','La Rioja'), ('Comunidad de Madrid','Comunidad de Madrid'), 
                  ('Extremadura','Extremadura'), ('Castilla La Mancha','Castilla La Mancha'), 
                  ('Comunidad Valenciana','Comunidad Valenciana'), 
                  ('Islas Baleares','Islas Baleares'), ('Andalucia','Andalucía'), 
                  ('Region de Murcia','Región de Murcia'), ('Islas Canarias','Islas Canarias')]
SEX_CHOICES= [('Hombre', 'Hombre'), ('Mujer', 'Mujer'), ('Prefiero no decirlo', 'Prefiero no decirlo')]

def validator_edad(edad):
    if edad > 120 or edad<0:
        raise ValidationError(
            _('%(edad)s is not a correct edad'),
            params={'value': edad},
        )

class Voter(models.Model):
    edad = models.IntegerField(validators=[validator_edad])
    region = models.CharField(max_length=50, choices=REGION_CHOICES, blank=True)
    profesion = models.TextField(max_length=50, blank=True)
    estudios = models.TextField(max_length=50, blank=True)
    sexo = models.CharField(max_length=20, choices=SEX_CHOICES, default='Prefiero no decirlo')
    Usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    def __str__(self):
        return self.Usuario.username
