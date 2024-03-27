import spotipy
from spotipy.oauth2 import SpotifyOAuth
import matplotlib as mpl
import matplotlib.pyplot as plt

scope = "user-library-read"

SPOTIPY_CLIENT_ID = open("client_id.txt","r").read()
SPOTIPY_CLIENT_SECRET = open("secret.txt","r").read()
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:9090"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope))


#Gets all the tracks in a playlist
def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

#Iterates through a playlist and returns the average of a feature
def itr_playlist(playlistID,feature):    
    count=0
    plSum=0
    plAvg=0
    audio={}
    tracks={}
    trList={}
    playlist=get_playlist_tracks(playlistID)
    while count < len(playlist)-1:
        tracks[count]=playlist[count]["track"]["name"]
        audio[tracks[count]]=sp.audio_features(playlist[count]["track"]["id"])
        plSum+=audio[tracks[count]][0][feature]
        plAvg=plSum/len(playlist)
        count+=1
    return plAvg

if __name__ == "__main__":
    playlistList=sp.category_playlists("Pop",limit=50)
    #playlistList.update(sp.category_playlists("Pop",limit=50,offset=50))
    #Uncomment to add 50 more playlists
    xplot=[]
    count=0
    while count < len(playlistList["playlists"]["items"])-1:
        playlist=playlistList["playlists"]["items"][count]["uri"]
        xplot.append([itr_playlist(playlist,"danceability")])
        count+=1
        print(count)
    print(xplot)
    yplot=[]
    count=0
    while count < len(playlistList["playlists"]["items"])-1:
        playlist=playlistList["playlists"]["items"][count]["uri"]
        yplot.append([itr_playlist(playlist,"valence")])
        count+=1
        print(count)
    print(yplot)
    figure,ax = plt.subplots(figsize=(5,2.7),layout="constrained")
    ax.scatter(xplot,yplot)
    plt.xlabel("Energy")
    plt.ylabel("Valence")
    plt.show()