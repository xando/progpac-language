from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from language import interpreter
from .models import Level


class LevelView(generics.RetrieveAPIView):
    model = Level


class Validate(APIView):
    def post(self, request, pk, format=None):
        res = interpreter.interpret(request.DATA.get('source', ''))
        return Response(res)
