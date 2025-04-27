from flask import request, jsonify, redirect, session
import requests
import os
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from models.User import User
from models.Group import Group
from models.Stats import Stats
from models.Match import Match
from models.UserGroup import UserGroup
from schemas.user_schema import UserSchema
from app import db
import json
from werkzeug.security import generate_password_hash, check_password_hash

user_schema = UserSchema()
users_schema = UserSchema(many=True)

api_key = 'RGAPI-6f4f0ac1-76bb-44d2-aa85-620f61b6592f'


def register():
    email = request.json['email']
    username = request.json['username']
    test_username = User.query.filter_by(username=username).first()
    if test_username:
        return jsonify(message='That username already exists', status=409), 409

    test_email = User.query.filter_by(email=email).first()
    if test_email:
        return jsonify(message='That email is already in use', status=409), 409
    else:
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        password = request.json['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        role = request.json['role'].capitalize()
        bio = request.json['bio']
        riot_name = request.json['riot_name']
        riot_tag = request.json['riot_tag']
        riot_region = request.json['riot_region'].lower()
        user = User(username=username, first_name=first_name, last_name=last_name, email=email, password=hashed_password, role=role, bio=bio, riot_name=riot_name, riot_tag=riot_tag, riot_region=riot_region, riot_puuid=None, discord_id=None)
        db.session.add(user)
        db.session.commit()

    riot_url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{riot_name}/{riot_tag}?api_key={api_key}"
    response = requests.get(riot_url)

    if response.status_code == 200:
        riot_data = response.json()
        user.riot_puuid = riot_data.get('puuid')
        db.session.commit()
    else:
        return jsonify(message='User created but Riot account linking failed', status=response.status_code), 202
    

    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{riot_data.get('puuid')}/ids?start=0&count=20"
    rank_url = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-puuid/{riot_data.get('puuid')}"

    rank_response = requests.get(rank_url, headers={'X-Riot-Token': api_key})
    response = requests.get(url, headers={'X-Riot-Token': api_key})

    if response.status_code != 200:
        return jsonify({'message': 'Error fetching matches'}), 500
    
    matches = response.json()
    rank_response = rank_response.json()

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
    last20kills = []
    last20deaths = []
    last20assists = []

    user.rank = rank_response[0]['tier'] if rank_response else 'Unranked'

    for match_id in matches:
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"

        response = requests.get(url, headers={'X-Riot-Token': api_key})

        if response.status_code != 200:
            return jsonify({'message': 'Error fetching match'}), 500
        
        match = response.json()

        part_index = match['metadata']['participants'].index(riot_data.get('puuid'))
        stats_list = match['info']['participants'][part_index]

        kills += stats_list['kills']
        deaths += stats_list['deaths']
        assists += stats_list['assists']
        wins += 1 if stats_list['win'] else 0
        losses += 0 if stats_list['win'] else 1
        rank = stats_list['summonerLevel']
        last20kills.append(stats_list['kills'])
        last20deaths.append(stats_list['deaths'])
        last20assists.append(stats_list['assists'])

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
        user.stats.last20kills = json.dumps(last20kills)
        user.stats.last20deaths = json.dumps(last20deaths)
        user.stats.last20assists = json.dumps(last20assists)

    else:
        stats = Stats(kills=kills, deaths=deaths, assists=assists, wins=wins, losses=losses, rank=rank, winloss=winloss, kda=kda, kapm=kapm, winpercent=winpercent, last20kills=json.dumps(last20kills), last20deaths=json.dumps(last20deaths), last20assists=json.dumps(last20assists), user=user)
        db.session.add(stats)

    db.session.commit()

    return jsonify(message='User and Riot account linked successfully', status=201), 201


def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))
        session['id'] = user.id
        return jsonify(message='Login succeeded!', access_token=access_token)
    else:
        return jsonify(message='Invalid email or password', status=401), 401


def add_user_to_group():
    # Get the data from the request (user_id and group_id)
    user_id = request.json.get('user_id')
    group_id = request.json.get('group_id')

    # Find the user and the group
    user = User.query.get(user_id)
    group = Group.query.get(group_id)

    if not user or not group:
        return jsonify({'message': 'User or Group not found'}), 404

    # Check if the link already exists (optional but recommended)
    existing_link = UserGroup.query.filter_by(user_id=user.id, group_id=group.id).first()
    if existing_link:
        return jsonify({'message': 'User already in group'}), 400

    # Create a new UserGroup link
    user_group = UserGroup(user_id=user.id, group_id=group.id)
    db.session.add(user_group)
    db.session.commit()

    return jsonify({'message': 'User added to group successfully'}), 200


def get_user(user):
    return jsonify(user.to_dict())

def get_users(user):
    data = request.get_json()

    liked_users = db.session.query(Match.liked_id).filter(Match.liker_id == user.id)
    liked_me = db.session.query(Match.liker_id).filter(Match.liked_id == user.id)

    query = User.query

    # Apply filters dynamically
    if "role" in data:
        query = query.filter(User.role == data["role"])
    if "rank" in data:
        query = query.filter(User.rank == data["rank"])

    excluded_ids = set([user.id])
    excluded_ids.update([row[0] for row in liked_users])
    excluded_ids.update([row[0] for row in liked_me])

    users_list = query.filter(~User.id.in_(excluded_ids)).all()
    result = [user.to_dict() for user in users_list]
    return jsonify(result)

def update_user(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.username = request.form['username']
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.bio = request.form['bio']
        user.role = request.form['role']
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.commit()
        return jsonify(message='You updated a profile', status=202), 202
    else:
        return jsonify(message='That profile does not exist', status=404), 404
    

def delete_user(user_id: int):
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(message='You deleted your profile', status=202), 202
    else:
        return jsonify(message='That profile does not exist', status=404), 404
    


DISCORD_CLIENT_ID = '1349024595683967007'
DISCORD_REDIRECT_URI = 'https://fmtbackendpy.onrender.com/discord_callback'
DISCORD_CLIENT_SECRET = 'HpJuvqB-gHgUAUT_KcLg1tkRrJN9MY-D'
DISCORD_API_BASE_URL = 'https://discord.com/api/'


def discord_login():
    discord_auth_url = f"https://discord.com/api/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={DISCORD_REDIRECT_URI}&response_type=code&scope=identify"
    return redirect(discord_auth_url)


def discord_callback(user):
    code = request.args.get('code')
    if not code:
        return jsonify(message='Authorization failed', status=400), 400

    data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': DISCORD_REDIRECT_URI,
        'scope': 'identify'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(f"{DISCORD_API_BASE_URL}/oauth2/token", data=data, headers=headers)

    #This is wrong, status code does not exist in response, change this tmr
    # if response.status_code != 200:
    #     return jsonify(message='Authorization failed when retrieving token response', status=400), 400
    
    response_data = response.json()
    access_token = response_data.get('access_token')
    token_type = response_data.get('token_type')

    headers = {
        'Authorization': f"{token_type} {access_token}"
    }
    user_response = f"{DISCORD_API_BASE_URL}/users/@me"

    # if user_response.status_code != 200:
    #     return jsonify(message='Authorization failed when retrieving user response', status=400), 400
    

    user_response = requests.get(user_response, headers=headers)
    user_data = user_response.json()
    discord_id = user_data.get('id')


    user.discord_id = discord_id
    db.session.commit()

    return redirect(f"http://localhost:5173/")





