from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from .models import Batter, Pitcher
from django.utils.safestring import mark_safe
import json


from .teamJang import *

def home(request):
    def home(request):

        rg = range(1, 13)
        # return render_to_response('game.html', {'rg': rg})
        return render(request, 'game/index.html', {'rg': rg})

def room(request, room_name):
    # model = Batter

    return render(request, 'game/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
    })


@csrf_exempt
def SearchPlayer(request):
    print("zzz")
    searchStr = request.POST['searchStr']
    print(searchStr)
    data = Batter.objects.all().filter(player=searchStr).order_by("-player")
    result = []

    for i in data:
        result.append({"year": i.year,
                       "team": i.team,
                       "position": i.position,
                       "player": i.player})

    return JsonResponse(result, safe=False)