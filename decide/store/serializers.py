from rest_framework import serializers

from .models import Vote


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    a = serializers.IntegerField()
    b = serializers.IntegerField()
    # sexo --> c = serializers.CharField()
    # edad --> d = serializer.IntegerField()
    # ip --> e = serializer.IPAddressField()
    # time --> f = serializer.TimeField()
    # ciudad -->  g = serializer.CharField()
    class Meta:
        model = Vote
        fields = ('voting_id', 'voter_id', 'a', 'b')
        #fields = ('voting_id', 'voter_id', 'a', 'b','c','d','e','f','g')
