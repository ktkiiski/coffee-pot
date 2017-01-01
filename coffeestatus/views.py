from django.conf import settings
from rest_framework import views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from webcam.models import Picture
from webcam.camera import take_picture
from coffeestatus.serializers import CommandSerializer
from collections import OrderedDict
import random


class CoffeeStatusView(views.APIView):

    serializer_class = CommandSerializer

    def post(self, request):
        return self.run_command(request.data)

    def get(self, request):
        return self.run_command(request.query_params)

    def run_command(self, request_data):
        required_token = settings.SLACK_COMMAND_TOKEN
        if required_token not in (request_data.get('token'), None):
            raise ValidationError({"token": "Invalid token"})
        request = self.request
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        if request_data.get('text') == 'now':
            # Force save a snapshot
            pictures = [take_picture()]
        else:
            pictures = list(Picture.objects.order_by('-created_at')[0:1])
        response_data = OrderedDict()
        response_data["response_type"] = "in_channel"
        response_data["text"] = random.choice(STATUS_TEXTS)
        response_data["attachments"] = [
            {
                "fallback": "Web camera snapshot",
                "image_url": request.build_absolute_uri(pic.image.url),
                "text": pic.description(),
            }
            for pic in pictures
        ]
        return Response(response_data, status=200)


STATUS_TEXTS = [
    "Here's what it looks like in the kitchen.",
    "Let's take a look at the kitchen, shall we?",
    "Let's see if there is any coffee!",
    "Oh, you want some coffee?",
    "Did someone say \"coffee\"?",
]
