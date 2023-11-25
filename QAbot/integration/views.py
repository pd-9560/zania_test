import json

from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from integration.serializers import UploadSerializer
from integration.bot.bot import Bot


class AnsweringBotAPIView(APIView):
    serializer_class = UploadSerializer

    def post(self, request, *args, **kwargs):
        context = request.FILES.get('context')
        questions = request.FILES.get('questions')
        if self.serializer_class(
            data={'context': context, 'questions': questions}
            ).is_valid() and questions.content_type == 'application/json':
            #  read questions
            questions.seek(0)
            try:
                questions = json.loads(questions.read()).get('questions')
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            # save context
            context_file_name = default_storage.save(context.name, context)
            context_file_path = str(settings.MEDIA_ROOT) + \
            "/" + str(context_file_name)
            
            bot = Bot()
            answers = bot.answer(context_file_path, questions)
            return Response(data=json.dumps(answers))
        return Response(status=status.HTTP_400_BAD_REQUEST)
