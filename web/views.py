import json

from django.http import JsonResponse, HttpResponseNotFound
from django.views.generic import View

from herbert import interpreter

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
        walk = interpreter.walk_world(level['content'], interpreted['code'])
        return JsonResponse({
            'interpreted': interpreted,
            'walk': walk
        })



class LevelsList(View):
    def get(self, request):
        return JsonResponse(levels.level_list(), safe=False)
