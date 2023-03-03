"""Run flask site, which use spotify api and create avaliable markets' map of song"""
import os
import json
import base64
from dotenv import load_dotenv
import requests
import folium
import pycountry
from flask import Flask, render_template, request

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def get_token():
    '''Function get token from your cliend id and secret'''
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
    '''Function find first autohr by your phrase'''
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
    """Function finds top songs by artist id"""
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=UA"
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result

def get_information_song(token, song_id):
    """Get information about song by song id"""
    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def create_map(availiable_markets):
    """Create map of all avaliable markets by song """
    with open('country.json', encoding='utf-8') as file:
        alpha_2_list = json.load(file)
    song_map = folium.Map(tiles="Stamen Terrain")
    fg_name = folium.FeatureGroup(name="Avaliable markets for top song")
    for market in availiable_markets:
        try:
            country_name = pycountry.countries.get(alpha_2=market)
            cordinate = alpha_2_list[market]
            fg_name.add_child(folium.Marker(location = cordinate,\
 popup=country_name.name, icon=folium.Icon()))
        except:
            continue
    song_map.add_child(fg_name)
    return song_map._repr_html_()


app = Flask(__name__)


@app.route('/')
@app.route('/entry')
def entry_page():
    return render_template('entry.html')


@app.route('/search4', methods=['POST'])
def do_search():
    phrase = request.form['phrase']
    token = get_token()
    artist_token = search_for_artist(token, phrase)['id']
    top_song_id = get_song_by_artist(token, artist_token)[0]['id']
    availiable_market = get_information_song(token, top_song_id)['available_markets']
    return create_map(availiable_market)



if __name__ == '__main__':
    app.run(debug = True)
