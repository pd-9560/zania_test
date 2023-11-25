from rest_framework.response import Response
from rest_framework.views import APIView

from integration.serializers import UploadSerializer


class AnsweringBotAPIView(APIView):
    serializer_class = UploadSerializer

    def post(self, request, *args, **kwargs):
        context = request.FILES.get('context')
        content_type = context.content_type
        return Response("Got it")
