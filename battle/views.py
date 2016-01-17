from django.shortcuts import render
from django.http import Http404, JsonResponse

from battle.models import Battle

def index(request):
    battles = Battle.objects.all()
    data = dict(battles=battles)
    return render(request, 'index.html', data)

def detail(request, battle_id):
    try:
        battle = Battle.objects.get(id=battle_id)
        battle_hashtags = battle.battlehashtags_set.all().prefetch_related('hashtag')
        data = dict(battle=battle, battle_hashtags=battle_hashtags)
    except Battle.DoesNotExist:
        raise Http404('Battle does not exist')
    return render(request, 'battle/details.html', data)
