from typing import Any

import spotipy
from dotenv import load_dotenv
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
