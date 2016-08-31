from rest_framework import serializers


class CommandSerializer(serializers.Serializer):
    token = serializers.CharField(required=False)
    team_id = serializers.CharField(required=False)
    team_domain = serializers.CharField(required=False)
    channel_id = serializers.CharField(required=False)
    channel_name = serializers.CharField(required=False)
    user_id = serializers.CharField(required=False)
    user_name = serializers.CharField(required=False)
    command = serializers.CharField(required=False)
    text = serializers.CharField(required=False)
    response_url = serializers.CharField(required=False)
