from django.db import models
from base.models import BigBigField


class Vote(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    #voter_age = models.PositiveIntegerField()
    #voter_ip = models.TextField()
    #voter_city = mdoels.TextField()

    a = BigBigField()
    b = BigBigField()

    voted = models.DateTimeField(auto_now=True)
    voter_sex = models.TextField()

    def __str__(self):
        return '{}: {}'.format(self.voting_id, self.voter_id)

        #self.voting_sex, self.voting_ip,self.voting_age añadir campos a visualizar en el panel 



