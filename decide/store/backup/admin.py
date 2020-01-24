from django.contrib import admin

from .models import Vote
from .models import Backup


admin.site.register(Vote)
#admin.site.register(Backup)
class BackupAdmin(admin.ModelAdmin):
    list_display = ('backup_date','backup_data')
    list_filter = ('backup_date',)
    search_fields = ('backup_date',)

admin.site.register(Backup, BackupAdmin)
