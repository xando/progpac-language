import os

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
        file_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', obj.file))
        content = open(file_path, 'r').read().strip().split()
        return content


class LevelView(generics.RetrieveAPIView):
    serializer_class = LevelSerializer
    model = models.Level


class LevelListView(generics.ListAPIView):
    serializer_class = LevelSerializer
    model = models.Level


class Validate(APIView):
    def post(self, request, pk, format=None):
        obj = models.Level.objects.get(hash=pk)
        file_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', obj.file))
        world = open(file_path, 'r').read().strip()
        interpreted = interpreter.interpret(request.DATA.get('source', ''))
        walk = interpreter.walk_world(world, interpreted['code'])
        return Response({
            'interpreted': interpreted,
            'walk': walk
        })

