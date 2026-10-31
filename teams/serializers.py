from rest_framework import serializers
from teams.models import Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = 'id', 'name', 'description', 'created_at','owner'
        read_only_fields = ('owner', 'created_at')
