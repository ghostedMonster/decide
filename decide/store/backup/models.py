from django.db import models
from base.models import BigBigField

class Backup(models.Model):
    backup_date = models.DateTimeField(auto_now=True)
    #Tengo que crear aquí el método para crear la copia de seguridad. Con el auto_now=True se le asigna valor automáticamente
    backup_data = BigBigField()

    def __str__(self):
        return '{}' .format(self.backup_date)
