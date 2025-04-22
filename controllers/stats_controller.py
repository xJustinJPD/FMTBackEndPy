import requests
from flask import request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from models.Stats import Stats
from models.User import User
from schemas.stats_schema import StatsSchema
from app import db, app

stats_schema = StatsSchema()
stats_schema = StatsSchema(many=True)

api_key = 'RGAPI-ab80418a-9d50-444e-a67d-82df810fc73b'
this_puuid = 'XVOMn2SnoNAokktURdg1V3FeXtSWJLJkZYFZMOjp9S3gDD6F-ypV_FTDdD0oE1HTB9ziRYcOfiznHw'
matches = []
match = {}

def get_matches():
    puuid = request.json.get('puuid')
    if not puuid:
        return jsonify({'message': 'No puuid provided'}), 400
    
    url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20'

    response = requests.get(url, headers={'X-Riot-Token': api_key})

    if response.status_code != 200:
        return jsonify({'message': 'Error fetching matches'}), 500
    
    matches = response.json()
    return jsonify(matches)


def get_match():
    match_id = request.json.get('match_id')
    if not match_id:
        return jsonify({'message': 'No match_id provided'}), 400
    
    url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}'

    response = requests.get(url, headers={'X-Riot-Token': api_key})

    if response.status_code != 200:
        return jsonify({'message': 'Error fetching match'}), 500
    
    match = response.json()

    part_index = match['metadata']['participants'].index(this_puuid)
    stats = match['info']['participants'][part_index]
    return jsonify(stats)


def get_stats():
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{this_puuid}/ids?start=0&count=20'

    response = requests.get(url, headers={'X-Riot-Token': api_key})

    if response.status_code != 200:
        return jsonify({'message': 'Error fetching matches'}), 500
    
    matches = response.json()

    kills = 0
    deaths = 0
    assists = 0
    wins = 0
    losses = 0
    rank = 0
    winloss = 0.0
    kda = 0.0
    kapm = 0.0
    winpercent = 0

    for match_id in matches:
        url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}'

        response = requests.get(url, headers={'X-Riot-Token': api_key})

        if response.status_code != 200:
            return jsonify({'message': 'Error fetching match'}), 500
        
        match = response.json()

        part_index = match['metadata']['participants'].index(this_puuid)
        stats_list = match['info']['participants'][part_index]

        kills += stats_list['kills']
        deaths += stats_list['deaths']
        assists += stats_list['assists']
        wins += 1 if stats_list['win'] else 0
        losses += 0 if stats_list['win'] else 1
        rank = stats_list['summonerLevel']

    winloss = wins / losses
    kda = (kills + assists) / deaths
    kapm = (kills + assists) / (wins + losses)
    winpercent = int(wins / (wins + losses) * 100)

    if user.stats:
        user.stats.kills = kills
        user.stats.deaths = deaths
        user.stats.assists = assists
        user.stats.wins = wins
        user.stats.losses = losses
        user.stats.rank = rank
        user.stats.winloss = winloss
        user.stats.kda = kda
        user.stats.kapm = kapm
        user.stats.winpercent = winpercent

    else:
        stats = Stats(kills=kills, deaths=deaths, assists=assists, wins=wins, losses=losses, rank=rank, winloss=winloss, kda=kda, kapm=kapm, winpercent=winpercent  ,user=user)
        db.session.add(stats)

    db.session.commit()

    return jsonify(message = "Stats added successfully"), 201