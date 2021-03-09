# -*- coding: utf-8 -*-
"""
Created on Mon March 8 13:03:35 2021

Create playlists based on a word with Spotipy

@author: Connor C
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pp
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO


# Use your own spotify dev data below!
# set open_browser=False to prevent Spotipy from attempting to open the default browser, authenticate with credentials
scope = 'user-library-read user-library-modify playlist-modify-public ugc-image-upload'
client_id = "ENTER YOU CLIENT ID HERE"
client_secret = "ENTER YOU CLIENT SECRET"
redirect_uri = "http://localhost:8888"
usernamevar = "ENTER YOUR USERNAME"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope))

offsetvar = 0
usedvalues = []
inputvar = input("Enter Name to Search:")

#create new playlist
sp.user_playlist_create(usernamevar, name=inputvar, description='ByTheBot')

def GetPlaylistID(username,playlist_name):
    playlist_id = ''
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:  # iterate through playlists I follow
        if playlist['name'] == playlist_name:  # filter for newly created playlist
            playlist_id = playlist['id']
    return playlist_id


img = Image.new('RGB', (500, 500), color = (1, 1, 1))
fnt = ImageFont.truetype('DancingScript-Bold.ttf', 80)
d = ImageDraw.Draw(img)
d.text((20,20), inputvar, font=fnt, fill=(255, 255, 255))
buffered = BytesIO()
img.save(buffered, format="JPEG")
img_str = base64.b64encode(buffered.getvalue())

sp.playlist_upload_cover_image(GetPlaylistID(usernamevar,inputvar),img_str)



while offsetvar < 300:
    tracks = sp.search(inputvar,limit=50,type="track",offset=offsetvar,market="US")
    for track in tracks['tracks']['items']:
        if track['name'].find('(') == -1:
            if track['name'].find('-') == -1:
                trimindex = 999
            else:
                trimindex = track['name'].find('-')
        else:
            trimindex = track['name'].find('(')
        if inputvar in track['name'][:trimindex]:
            if "ft. "+inputvar not in track['name'][:trimindex] and "feat. "+inputvar not in track['name'][:trimindex] and "- "+inputvar not in track['name'][:trimindex]:
                if "Soundtrack" not in track['album']['name']:
                    if [track['name'][:trimindex].strip(),track['artists'][0]['name']] not in usedvalues:
                        pp(track['name'][:trimindex].strip())
                        usedvalues.append([track['name'][:trimindex].strip(),track['artists'][0]['name']])
                        sp.user_playlist_add_tracks(usernamevar, GetPlaylistID(usernamevar,inputvar), [track["uri"][14:]])
    offsetvar += 50
