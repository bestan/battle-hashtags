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

    winner = battle.get_winner()
    data['winner'] = winner.hashtag.value if winner else None

    winner_by_ratio = battle.get_winner_by_ratio()
    data['winner_by_ratio'] = winner_by_ratio.hashtag.value if winner_by_ratio else None

    return render(request, 'battle/details.html', data)

def api_detail(request, battle_id):
    try:
        battle = Battle.objects.get(id=battle_id)
    except Battle.DoesNotExist:
        raise Http404('Battle does not exist')

    battle_hashtags = battle.battlehashtags_set.all().prefetch_related('hashtag')

    data = dict()
    data['name'] = battle.name
    data['start_time'] = battle.start_time
    data['end_time'] = battle.end_time

    winner = battle.get_winner()
    data['winner'] = winner.hashtag.value if winner else None

    winner_by_ratio = battle.get_winner_by_ratio()
    data['winner_by_ratio'] = winner_by_ratio.hashtag.value if winner_by_ratio else None

    data['hashtags'] = [x.to_dict() for x in battle_hashtags]

    return JsonResponse(data)
