from django.db import models


class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    def samplingfraction(self, census, voters):
        res = float((voters/census)*100)

        if census != 0:
            res = round(res, 4)
        else:
            res = 0

        return float(res)

    def elevationcoefficient(self, census, voters):
        res = float(census/voters)

        if voters != 0:
            res = round(res, 4)
        else:
            res = 0

        return float(res)

    class Meta:
        unique_together = (('voting_id', 'voter_id'),)
