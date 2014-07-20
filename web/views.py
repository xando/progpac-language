from rest_framework.views import APIView
from rest_framework.response import Response

from language import interpreter


class Validate(APIView):
    def post(self, request, format=None):
        res = interpreter.interpret(request.DATA.get('source', ''))
        return Response(res)
