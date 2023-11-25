from rest_framework.serializers import Serializer, FileField, JSONField


class UploadSerializer(Serializer):
    context = FileField()
    questions = JSONField()

    class Meta:
        fields = ['context', 'questions', ]
