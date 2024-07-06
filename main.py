from typing import Any

import mpv
import requests
import spotipy
from dotenv import load_dotenv
from pynput import keyboard
from spotipy.oauth2 import SpotifyOAuth


def get_tracks(sp: spotipy.Spotify, query: str) -> dict[str, list[str]]:
    names = []
    links = []
    artists = []
    results: Any = sp.search(query, type="track", limit=5)

    for item in results["tracks"]["items"]:
        names.append(item["name"])
        links.append(item["external_urls"]["spotify"])
        for artist in item["artists"]:
            artists.append(artist["name"])

    return {"names": names, "links": links, "artists": artists}


def get_artists(sp: spotipy.Spotify, query: str) -> dict[str, list[str]]:
    names = []
    links = []
    results: Any = sp.search(query, type="artist")

    for items in results["artists"]["items"]:
        names.append(items["name"])
        links.append(items["external_urls"]["spotify"])

    return {"names": names, "links": links}


def get_album(sp: spotipy.Spotify, query: str) -> dict[str, list[str]]:
    names = []
    links = []
    results: Any = sp.search(query, type="album")

    for items in results["artists"]["items"]:
        names.append(items["name"])
        links.append(items["external_urls"]["spotify"])

    return {"names": names, "links": links}


def playback(query: str) -> str | None:
    song_link = ""
    links = []
    explicit_content = []
    url = "https://saavn.dev/api/search/songs"

    response = requests.get(url, params={"query": query}).json()
    for results in response["data"]["results"]:
        links.append(results["url"])
        explicit_content.append(results["explicitContent"])
    song = {"links": links, "explicitContent": explicit_content}
    print(song)

    explicit = True
    for index, explicit_content in enumerate(song["explicitContent"]):
        if explicit_content == explicit:
            song_link = song["links"][index]
            break
        elif song_link == "":
            song_link = song["links"][index]

    print(song_link)
    player = mpv.MPV(ytdl=True)
    player.play(song_link)

    # Define the function to handle key presses
    def on_press(key):
        try:
            # Check if the space bar is pressed
            if key == keyboard.Key.space:
                player.pause = not player.pause
        except AttributeError:
            pass

    # Set up the key listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Keep the script running
    listener.join()


def main() -> None:
    load_dotenv()
    scope = "user-library-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    album_name = input("Enter an album name: ")
    album_links = get_album(sp, album_name)
    for album_link in album_links:
        print(album_link)


if __name__ == "__main__":
    main()
