from django.shortcuts import render
from django.http import HttpResponse
import requests


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def score_view(request):
    return render(request, "templates/score_view.html")


def search_result(request):
    if request.method == "GET":
        summoner_name = request.Get.get("search_text")

        summoner_exist = False
        sum_result = {}
        solo_tier = {}
        team_tier = {}
        store_list = []
        game_list = {}
        game_list2 = []
        api_key = "Riot_API_key"

        summoner_url = (
            "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
            + str(summoner_name)
        )
        params = {"api_key": api_key}
        res = requests.get(summoner_url, params=params)

        if res.status_code == 200:
            summoner_exist = True
            summoners_result = res.json()
            if summoners_result:
                sum_result["name"] = summoners_result["name"]
                sum_result["level"] = sum_result["summonerLevel"]
                sum_result["profileIconId"] = summoners_result["profileIconId"]

                tier_url = (
                    "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"
                    + summoners_result["id"]
                )
                tier_info = requests.get(tier_url, params=params)
                tier_info = tier_info.json()

                if len(tier_info) == 1:
                    tier_info = tier_info.pop()
                    if tier_info["queueType"] == "RANKED_FLEX_SR":
                        team_tier["rank_type"] = "자유랭크 5:5"
                        team_tier["tier"] = tier_info["tier"]
                        team_tier["rank"] = tier_info["rank"]
                        team_tier["points"] = tier_info["points"]
                        team_tier["wins"] = tier_info["wins"]
                        team_tier["losses"] = tier_info["losses"]
                    else:
                        solo_tier["rank_type"] = "솔로랭크 5:5"
                        solo_tier["tier"] = tier_info["tier"]
                        solo_tier["rank"] = tier_info["rank"]
                        solo_tier["points"] = tier_info["leaguePoints"]
                        solo_tier["wins"] = tier_info["wins"]
                        solo_tier["losses"] = tier_info["losses"]

                if len(tier_info) == 2:  # 자유랭크, 솔로랭크 둘다 전적이 있는경우
                    for item in tier_info:
                        store_list.append(item)
                    solo_tier['rank_type'] = '솔로랭크 5:5'
                    solo_tier['tier'] = store_list[0]['tier']
                    solo_tier['rank'] = store_list[0]['rank']
                    solo_tier['points'] = store_list[0]['leaguePoints']
                    solo_tier['wins'] = store_list[0]['wins']
                    solo_tier['losses'] = store_list[0]['losses']

                    team_tier['rank_type'] = '자유랭크 5:5'
                    team_tier['tier'] = store_list[1]['tier']
                    team_tier['rank'] = store_list[1]['rank']
                    team_tier['points'] = store_list[1]['leaguePoints']
                    team_tier['wins'] = store_list[1]['wins']
                    team_tier['losses'] = store_list[1]['losses']

        return render(request, 'score/search_result.html', {'summoner_exist': summoner_exist, 'summoners_result': sum_result, 'solo_tier': solo_tier, 'team_tier': team_tier})

# Create your views here.
