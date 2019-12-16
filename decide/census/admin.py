from django.contrib import admin

from .models import Census


class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting_name', 'voter_id')
    list_filter = ('voting_name', )

    search_fields = ('voter_id', )


admin.site.register(Census, CensusAdmin)
