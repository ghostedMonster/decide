from django.contrib import admin
from background_task import background

from .models import Vote
from .models import Backup

import os
from django.core import management
from django.conf import settings
from django_cron import CronJobBase, Schedule
import django_crontab

admin.site.register(Vote)

class BackupAdmin(admin.ModelAdmin):
    management.call_command('runcrons')
    management.call_command('dbbackup')

admin.site.register(Backup, BackupAdmin)


