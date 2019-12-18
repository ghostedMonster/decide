from django.db import models
from base.models import BigBigField


class Vote(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()
    

    a = BigBigField()
    b = BigBigField()

    voted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {}'.format(self.voting_id, self.voter_id)
        #self.voting_sex, self.voting_ip,self.voting_age añadir campos a visualizar en el panel
        """from django.contrib.gis.utils import GeoIP
            g = GeoIP()
            ip = request.META.get('REMOTE_ADDR', None)
            if ip:
                city = g.city(ip)['city']
            else:
                city = 'Rome' # default city"""

