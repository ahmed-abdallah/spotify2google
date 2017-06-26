import sys
import getpass

import spotipy
import spotipy.util as util
from gmusicapi import Mobileclient

SPOTIFY_CLIENT_ID = 'CLIENT_ID'
SPOTIFY_CLIENT_SECRET = 'CLIENT_SECRET'

g_username = input('Google Play username: ')
g_password = getpass.getpass('Google Play password: ')
g_playlist_name = input('New playlist name (empty to keep name): ')
s_playlist_url = input('Spotify playlist URL: ')

# get spotify url params
spotify_user_id = 0
spotify_playlist_id = ''

path_data = s_playlist_url.split('/')
for path_piece in range(len(path_data)):
    if path_data[path_piece] == 'user':
        spotify_user_id = path_data[path_piece+1]
    if path_data[path_piece] == 'playlist':
        spotify_playlist_id = path_data[path_piece+1]



# authenticate
gapi = Mobileclient()
logged_in = gapi.login(g_username, g_password, Mobileclient.FROM_MAC_ADDRESS)
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# get playlist
playlist = sp.user_playlist(spotify_user_id, spotify_playlist_id)
track_response = playlist['tracks']
gplaylist = []

for song in track_response['items']:
    song_search_string = "%s - %s" % (song['track']['artists'][0]['name'], song['track']['name'])
    song_result = gapi.search(song_search_string)
    gplaylist.append(song_result['song_hits'][0]['track']['storeId'])

if g_playlist_name == '':
    g_playlist_name = playlist['name']

playlist_id = gapi.create_playlist(g_playlist_name, 'Imported From Spotify')

gapi.add_songs_to_playlist(playlist_id, gplaylist)
