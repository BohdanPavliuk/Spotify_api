from dotenv import load_dotenv
import os
import base64
from requests import post
import requests
import json



def get_token():
    """Function get spotify token"""
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded" 
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers = headers, data = data) 
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    """Function search for author by phrase"""
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None

    return json_result[0]

def get_song_by_artist(token, artist_id):
    """Get top songs of author"""
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=UA"
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result

def get_information_song(token, song_id):
    """Function get information of song"""
    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result



if __name__ == '__main__':
    load_dotenv()

    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    print('Input the name of author, you want to get')
    artist_name = input('>>> ')
    token = get_token()
    artist_info = search_for_artist(token, artist_name)
    if not artist_info:
        os.exit('No artist is found')
    artist_id = artist_info['id']
    songs = get_song_by_artist(token, artist_id) 
    id_track = songs[0]['id']
    top_song_info = get_information_song(token, id_track)
    users_wants = ['artist_name', 'artist_id', 'artist_genre', 'top_songs', 'avaliable_markets_for_best_song']
    dct_get = {1: artist_info['name'], 2: artist_id, 3: artist_info['genres'], 5: top_song_info['available_markets']}
    for idx, info in enumerate(users_wants):
        print(f'{idx + 1}. {info}')
    to_choose = ''
    while not (to_choose.isnumeric() and 1<=int(to_choose)<=5):
        print('Put number of information, you want to get')
        to_choose = input('>>> ')
    to_choose = int(to_choose)
    if to_choose in dct_get:
        print(dct_get[to_choose])
    else:
        for idx, song in enumerate(songs):
            print(f"{idx+1}. {song['name']}")