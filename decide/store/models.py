from django.db import models
from base.models import BigBigField
from django.core.files.storage import default_storage
from django.core import management
from django.conf import settings
from django_cron import CronJobBase, Schedule
import os
import dbbackup

class Vote(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    a = BigBigField()
    b = BigBigField()

    voted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {}'.format(self.voting_id, self.voter_id)

class Backup(models.Model):
    #backup_date = models.DateTimeField(auto_now=True)
    #Tengo que crear aquí el método para crear la copia de seguridad. Con el auto_now=True se le asigna valor automáticamente
    #backup_name = models.TextField()
    #backup_path = os.curdir + 'backup/'
    management.call_command('runcrons')
    #management.call_command('dbbackup')
    #def __str__(self):
        #return '{}' .format(self)
