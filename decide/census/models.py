from django.db import models


class Census(models.Model):
    voting_name = models.CharField(max_length=200)
    voter_id = models.PositiveIntegerField()

    class Meta:
        unique_together = (('voting_name', 'voter_id'),)
