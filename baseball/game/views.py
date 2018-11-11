from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from .models import Batter, Pitcher
from django.utils.safestring import mark_safe
import json
from .teamJang import *

def home(request):
    rg = range(1, 13)
    return render(request, 'game/game.html', {'rg': rg})


def room(request):
    rg = range(1, 13)

    return render(request, 'game/game.html', {
        'room_name_json': mark_safe(json.dumps('baseball')),
        'rg': rg,
    })


@csrf_exempt
def SearchPlayer(request):
    print("SearchPlayer IN")
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

@csrf_exempt
def searchByYear(request):
    print("searchByYear IN")
    selectedYear = request.POST['year']
    print("searchByYear = ", selectedYear)
    data = Batter.objects.filter(year=selectedYear).distinct().values()
    result = []

    for index, item in enumerate(data):
        if result.count(item['team']) >= 1:
            continue

        result.append(item['team'])

    return JsonResponse(result, safe=False)


@csrf_exempt
def getBatters(request):
    print("getBatters IN")

    selectedYear = request.POST['year']
    selectedTeam = request.POST['team']
    selectedPosition = request.POST['position']

    positionDict = {'포수':'C', '1루수':'1B', '2루수':'2B', '3루수':'3B',
                    '유격수':'SS', '좌익수':'LF', '중견수':'CF',
                    '우익수':'RF', '지명타자':'DF'}

    player = Batter.objects.filter(year=int(selectedYear)).filter(team=selectedTeam)\
                            .filter(position=positionDict[selectedPosition]).values()

    result = []

    for item in player:
        result.append(item)

    return JsonResponse(result, safe=False)



@csrf_exempt
def getPitchers(request):
    print("getPitchers IN")

    selectedYear = request.POST['year']
    selectedTeam = request.POST['team']

    player = Pitcher.objects.filter(year=selectedYear).filter(team=selectedTeam).values()

    result = []

    for item in player:
        result.append(item)

    return JsonResponse(result, safe=False)