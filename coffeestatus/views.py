from rest_framework import views
from rest_framework.response import Response
from webcam.models import Picture
from coffeestatus.serializers import CommandSerializer
from collections import OrderedDict


class CoffeeStatusView(views.APIView):

    serializer_class = CommandSerializer

    def post(self, request):
        return self.run_command(request.data)

    def get(self, request):
        return self.run_command(request.query_params)

    def run_command(self, request_data):
        request = self.request
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        response_data = OrderedDict()
        response_data["text"] = "Here's what it looks like at the kitchen."
        response_data["attachments"] = [
            {"image_url": request.build_absolute_uri(pic.image.url)}
            for pic in Picture.objects.order_by('-created_at')[0:1]
        ]
        return Response(response_data, status=200)
