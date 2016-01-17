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
    except Battle.DoesNotExist:
        raise Http404('Battle does not exist')

    battle_hashtags = battle.battlehashtags_set.all().prefetch_related('hashtag')
    data = dict(battle=battle, battle_hashtags=battle_hashtags)

    return render(request, 'battle/details.html', data)

def api_detail(request, battle_id):
    try:
        battle = Battle.objects.get(id=battle_id)
    except Battle.DoesNotExist:
        raise Http404('Battle does not exist')

    battle_hashtags = battle.battlehashtags_set.all().prefetch_related('hashtag')
    winner = battle_hashtags.order_by('typos').first()

    data = dict()
    data['name'] = battle.name
    data['start_time'] = battle.start_time
    data['end_time'] = battle.end_time
    data['winner'] = dict(typos=winner.typos, hashtag=winner.hashtag.to_dict())
    data['hashtags'] = [x.hashtag.to_dict() for x in battle_hashtags]

    return JsonResponse(data)
