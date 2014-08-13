import json

from django.http import JsonResponse, HttpResponseNotFound
from django.views.generic import View

from herbert import interpreter, solve

from . import levels

class Level(View):

    def get(self, request, key):
        level = levels.level_get(key)
        if not level:
            return HttpResponseNotFound()
        return JsonResponse(level)

    def post(self, request, key):
        level = levels.level_get(key)
        if not level:
            return HttpResponseNotFound()

        data = json.loads(request.body)

        interpreted = interpreter.interpret(data.get('source', ''))
        walk = solve.walk(level, interpreted['code'], interpreted['length'])

        return JsonResponse({
            'interpreted': interpreted,
            'walk': walk
        })



class LevelsList(View):
    def get(self, request):
        return JsonResponse(levels.level_list(), safe=False)
