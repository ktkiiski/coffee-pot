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
                    "Instead, look how cute this wombat is!",
            "attachments": [{
                "image_url": "https://s.yimg.com/ea/img/-/150828/womabt_1atvht1-1atvi0t.jpg",
            }],
        }
        return Response(response_data, status=200)
