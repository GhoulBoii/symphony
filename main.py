from typing import Any

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


# with open("results.txt", "w") as file:
#     file.write(json.dumps(results, indent=2))

# results = sp.current_user_saved_tracks()
# print(results)
# for idx, item in enumerate(results["items"]):
#     track = item["track"]
#     print(idx, track["artists"][0]["name"], " – ", track["name"])


# Retrieves Album Links
def get_album(sp, album_name: str) -> list[Any]:
    album_links = []
    results: Any = sp.search(album_name, type="album")
    for item in results["albums"]["items"]:
        album_links.append(item["external_urls"]["spotify"])
    return album_links


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
