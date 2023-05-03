import json
import spotipy
from datetime import datetime
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
ELNINO_ID = "1Rb9dhbiai9ZwuoDgHYA7w"

def get_datetime(release_date):
    return datetime.strptime(release_date, "%Y-%m-%d")

def sort_by_date(song):
    return get_datetime(song["release_date"]).timestamp()

def format_date(date):
    return get_datetime(date).strftime("%d %b %Y")

def get_all_artist_albums():

    elnino_url = 'spotify:artist:1Rb9dhbiai9ZwuoDgHYA7w'


    results = spotify.artist_albums(elnino_url)
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    return albums

def get_albums(album_ids):
    albums_info = spotify.albums(album_ids)
    return albums_info["albums"]

def get_album_artists(album):
    artists = set()
    album_tracks = album["tracks"]["items"]
    for track in album_tracks:
        artists.update([artist["name"] for artist in track["artists"] if artist["id"] != ELNINO_ID])

    return artists

def get_featured_artists(artists):
    if len(artists) > 2:
        return "Various artists"
    
    elif len(artists) > 0 or len(artists) <= 2:
        return " & ".join(artists)
    
    return ""

def get_recent_albums():
    albums = get_all_artist_albums()
    albums.sort(reverse=True, key=sort_by_date)
    elnino_spotify_information = []

    all_album_ids = [album["id"] for album in albums]
    album_full_info = []

    for i in range(0, len(all_album_ids), 20):
        id_range = all_album_ids[i:min(len(all_album_ids), i+20)]
        album_full_info.extend(get_albums(id_range))

    for album in album_full_info:
        artists_on_album = get_album_artists(album)
        is_ep = album["album_type"] == "single" and album["total_tracks"] > 1
        elnino_spotify_information.append({
            "name": album["name"],
            "image": album["images"][0],
            "type": "EP" if is_ep else album["album_type"],
            "date": format_date(album["release_date"]),
            "id": album["id"],
            "featured": get_featured_artists(artists_on_album)
        })

    return elnino_spotify_information

def write_recent_albums():
    with open("./songs.json", "w") as f:
        json.dump(get_recent_albums(), f)

def load_recent_albums():
    with open("./songs.json", "r") as f:
        data = json.load(f)

    return data

def format_song_name(album):
    return f" Title: {album['name']} (feat. {album['featured'] }) - {album['type'].title()}"

if __name__ == "__main__":
    write_recent_albums()