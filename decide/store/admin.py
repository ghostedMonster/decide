from django.contrib import admin

from .models import Vote



#admin.site.register(Vote)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voting_id','voter_id', 'voted','voter_sex','voter_ip')
    list_filter = ('voter_sex','voter_city')
    ordering =('voter_sex','voter_ip')
    search_fields = ('voting_id',)

