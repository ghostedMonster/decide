from rest_framework import serializers

from .models import Vote


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    a = serializers.IntegerField()
    b = serializers.IntegerField()

    voted = serializers.TimeField()
    # sexo 
    voter_sex = serializers.SerializerMethodField('definir_sexo')
    
    def definir_sexo(self, foo):
        return foo.name == "Hombre"
        
    # edad 
    voter_age = serializers.IntegerField()
    # ip 
    voter_ip = serializers.IPAddressField()
    # time
    voting_time = serializers.TimeField()
    # ciudad
    voter_city = serializers.CharField()
    class Meta:
        model = Vote
        fields = ('voting_id', 'voter_id', 'a', 'b','voter_sex','voted')
        #fields = ('voting_id', 'voter_id', 'a', 'b')
