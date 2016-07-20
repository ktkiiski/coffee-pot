from rest_framework import serializers


class CommandSerializer(serializers.Serializer):
    token = serializers.CharField()
    team_id = serializers.CharField()
    team_domain = serializers.CharField()
    channel_id = serializers.CharField()
    channel_name = serializers.CharField()
    user_id = serializers.CharField()
    user_name = serializers.CharField()
    command = serializers.CharField()
    text = serializers.CharField()
    response_url = serializers.CharField()
