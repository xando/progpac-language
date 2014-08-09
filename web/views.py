from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, serializers

from herbert import interpreter
from . import models


class LevelSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField('get_content')

    class Meta:
        model = models.Level

    def get_content(self, obj):
        content = open(obj.file, 'r').read().strip().split()
        # assert len(content) == len(content[0])
        return content


class LevelView(generics.RetrieveAPIView):
    serializer_class = LevelSerializer
    model = models.Level


class LevelListView(generics.ListAPIView):
    serializer_class = LevelSerializer
    model = models.Level


class Validate(APIView):
    def post(self, request, pk, format=None):
        level = models.Level.objects.get(hash=pk)
        world = open(level.file, 'r').read().strip()
        res = interpreter.interpret(request.DATA.get('source', ''))
        interpreter.walk_world(world, res['code'])
        return Response(interpreter.walk_world(world, res['code']))
