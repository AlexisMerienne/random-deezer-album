from flask import Flask, jsonify
import requests
import random

app = Flask(__name__)

DEEZER_SEARCH_API = "https://api.deezer.com/search"
DEEZER_ALBUM_URI = "https://www.deezer.com/fr/album/"


def get_random_number():
    return random.randint(1, 9999)


def get_random_album():
    random_number = get_random_number()
    api_url = f"{DEEZER_SEARCH_API}?q={random_number}&type=album"

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json().get("data", [])
        if data:
            random_track = random.choice(data)
            album_info = {
                "deezer_uri": DEEZER_ALBUM_URI+random_track["album"]["id"],
                "cover_medium": random_track["album"]["cover_medium"],
                "title": random_track["album"]["title"],
                "artist_name": random_track["artist"]["name"],
            }
            return album_info
    return None


@app.route("/random_album", methods=["GET"])
def random_album():
    album_info = get_random_album()

    if album_info:
        return jsonify(album_info), 200
    else:
        return jsonify({"error": "Unable to fetch random album"}), 500


if __name__ == "__main__":
    app.run(debug=True)
