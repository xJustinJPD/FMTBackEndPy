import requests
from flask import request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from models.Stats import Stats
from schemas.stats_schema import StatsSchema
from app import db, app

stats_schema = StatsSchema()
stats_schema = StatsSchema(many=True)

api_key = 'RGAPI-ed522daf-de38-4dae-af08-e68518faaaff'
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
    url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{this_puuid}/ids?start=0&count=20'

    response = requests.get(url, headers={'X-Riot-Token': api_key})

    if response.status_code != 200:
        return jsonify({'message': 'Error fetching matches'}), 500
    
    matches = response.json()

    kills = 0

    for match_id in matches:
        url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}'

        response = requests.get(url, headers={'X-Riot-Token': api_key})

        if response.status_code != 200:
            return jsonify({'message': 'Error fetching match'}), 500
        
        match = response.json()

        part_index = match['metadata']['participants'].index(this_puuid)
        stats_list = match['info']['participants'][part_index]
        kills = kills + stats_list['kills']

    return jsonify(kills)