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
    results: Any = sp.search(query, type="artist", limit=5)

    for items in results["artists"]["items"]:
        names.append(items["name"])
        links.append(items["external_urls"]["spotify"])

    return {"names": names, "links": links}


def get_artist_albums(sp: spotipy.Spotify, link: str) -> dict[str, list[str]]:
    names = []
    links = []
    results: Any = sp.artist_albums(artist_id=link)
    for item in results["items"]:
        names.append(item["name"])
        links.append(item["external_urls"]["spotify"])

    return {"names": names, "links": links}


def get_artist_top_tracks(sp: spotipy.Spotify, link: str) -> dict[str, list[str]]:
    names = []
    links = []
    results: Any = sp.artist_top_tracks(artist_id=link)
    for item in results["tracks"]:
        names.append(item["name"])
        links.append(item["external_urls"]["spotify"])

    return {"names": names, "links": links}


def get_related_artists(sp: spotipy.Spotify, link: str) -> dict[str, list[str]]:
    names = []
    links = []
    results: Any = sp.artist_related_artists(artist_id=link)
    for item in results["artists"]:
        names.append(item["name"])
        links.append(item["external_urls"]["spotify"])

    return {"names": names, "links": links}


def get_albums(sp: spotipy.Spotify, query: str) -> dict[str, list[str]]:
    names = []
    links = []
    results: Any = sp.search(query, type="album", limit=5)

    for items in results["albums"]["items"]:
        names.append(items["name"])
        links.append(items["external_urls"]["spotify"])

    return {"names": names, "links": links}


def get_album_tracks(sp: spotipy.Spotify, query: str) -> dict[str, list[str]]:
    names = []
    links = []
    results: Any = sp.album_tracks(album_id=query)
    for item in results["items"]:
        names.append(item["name"])
        links.append(item["external_urls"]["spotify"])

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
    song = {"links": links, "explicit_content": explicit_content}

    explicit_status = True
    for index, explicit_content in enumerate(song["explicit_content"]):
        if explicit_content == explicit_status:
            song_link = song["links"][index]
            break
        elif song_link == "":
            song_link = song["links"][index]

    player = mpv.MPV(ytdl=True)
    player.play(song_link)

    def on_press(key):
        try:
            if key == keyboard.Key.space:
                player.pause = not player.pause
        except AttributeError:
            pass

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()


def main() -> None:
    load_dotenv()
    scope = "user-library-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    print("Welcome to Symphony!")
    print("1) Home")
    print("2) Search Songs")
    print("3) Search Albums")
    print("4) Search Artists")
    option = int(input("Select an option to use: "))

    if option == 2:
        song_query = input("Enter a song name: ")
        tracks = get_tracks(sp, query=song_query)
        print("SONGS:")
        for index, (name, artist) in enumerate(zip(tracks["names"], tracks["artists"])):
            print(f"{index+1} - {name} by {artist}")
        print("-" * 50)

        index_input = int(input("Enter song index that you want to play: "))
        index_input -= 1
        playback(
            query=f'{tracks["names"][index_input]} - {tracks["artists"][index_input]}'
        )

    if option == 3:
        album_query = input("Enter an album: ")
        albums = get_albums(sp, query=album_query)
        print("ALBUMS:")
        for index, name in enumerate(albums["names"]):
            print(f"{index+1} - {name}")
        print("-" * 50)

        index_input = int(input("Enter album index: "))
        index_input -= 1
        album_tracks = get_album_tracks(sp, query=albums["links"][index_input])
        print("ALBUM TRACKS:")
        for index, album_track in enumerate(album_tracks["names"]):
            print(f"{index+1} - {album_track}")

    if option == 4:
        artist_query = input("Enter an artist: ")
        artists = get_artists(sp, query=artist_query)

        print("ARTISTS:")
        for index, name in enumerate(artists["names"]):
            print(f"{index+1} - {name}")
        print("-" * 50)

        index_input = int(input("Enter artist index: "))
        index_input -= 1

        artist_tracks = get_artist_top_tracks(sp, artists["links"][index_input])
        artist_albums = get_artist_albums(sp, artists["links"][index_input])
        related_artists = get_related_artists(sp, artists["links"][index_input])
        print("ARTIST TRACKS:")
        for index, artist_track in enumerate(artist_tracks["names"]):
            print(f"{index+1} - {artist_track}")
        print("-" * 50)

        print("ARTIST ALBUMS:")
        for index, artist_albums in enumerate(artist_albums["names"]):
            print(f"{index+1} - {artist_albums}")
        print("-" * 50)

        print("RELATED ARTISTS:")
        for index, related_artist in enumerate(related_artists["names"]):
            print(f"{index+1} - {related_artist}")
        print("-" * 50)


if __name__ == "__main__":
    main()
