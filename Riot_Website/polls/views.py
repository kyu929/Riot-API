from django.shortcuts import render
from django.http import HttpResponse
import requests


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def score_view(request):
    return render(request, 'templates/score_view.html')


def search_result(request):
    if request.method == "GET":
        summoner_name = request.Get.get('search_text')

        summoner_exist = False
        sum_result = {}
        solo_tier = {}
        team_tier = {}
        store_list = []
        game_list = {}
        game_list2 = []
        api_key = 'Riot_API_key'

        summoner_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summoner_name) 
        params = {'api_key': api_key}
        res = requests.get(summoner_url, params=params)

        if res.status_code == requests.codes.ok:
            summoner_exist = True
            summoners_result = res.json()
            if summoners_result:
                sum_result['name'] = summoners_result['name']
                sum_result['level'] = sum_result['summonerLevel']
##
# Create your views here.