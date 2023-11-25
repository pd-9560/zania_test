from rest_framework.serializers import Serializer, FileField, JSONField


class UploadSerializer(Serializer):
    context = FileField()
    questions = FileField()

    class Meta:
        fields = ['context', 'questions', ]
