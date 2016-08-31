from rest_framework import views
from rest_framework.response import Response
from .serializers import CommandSerializer


class CoffeeStatusView(views.APIView):

    serializer_class = CommandSerializer

    def post(self, request):
        return self.run_command(request.data)

    def get(self, request):
        return self.run_command(request.query_params)

    def run_command(self, request_data):
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        response_data = {
            "text": "Hello, I'm a coffee bot! Unfortunately, my camera module is not installed yet. "
                    "Please, pretend that this one is a photo of our coffee pot.",
            "attachments": [{
                "image_url": "http://ak1.ostkcdn.com/img/mxc/091020_coffee-pot.jpg",
            }],
        }
        return Response(response_data, status=200)
