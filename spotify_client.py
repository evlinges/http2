import pandas as pd
import base64
import requests

CLIENT_ID = "1fcce64ef2554e6d826a2ccd35e312de"
CLIENT_SECRET = "53d042fd41a3496c934ca22e9551c039"

def get_access_token():
    url = "https://accounts.spotify.com/api/token"

    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()

    return response.json()["access_token"]

# 3. GET-запит: інформація про артиста
def get_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def search_tracks(token, query):
    """
    Пошук треків через Spotify Search API.
    """
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": query,
        "type": "track",
        "limit": 5
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def save_to_csv(search_result, filename="tracks.csv"):
    """
    Збереження результатів пошуку у CSV файл.
    """
    tracks = []

    for item in search_result["tracks"]["items"]:
        tracks.append({
            "track_name": item["name"],
            "artist": item["artists"][0]["name"],
            "album": item["album"]["name"],
            "popularity": item["popularity"]
        })

    df = pd.DataFrame(tracks)
    df.to_csv(filename, index=False)
    print(f"\nCSV-файл '{filename}' успішно створено!")



# 4. Головна функція
def main():
    token = get_access_token()
    print("\n=== ACCESS TOKEN ОТРИМАНО УСПІШНО ===")
    print(token)

    # 1. Інформація про артиста
    artist_id = "1Xyo4u8uXC1ZmMpatF05PJ"  # The Weeknd
    artist = get_artist(token, artist_id)

    print("\n=== ІНФОРМАЦІЯ ПРО АРТИСТА ===")
    print("Ім'я:", artist["name"])
    print("Популярність:", artist["popularity"])
    print("Жанри:", ", ".join(artist["genres"]))
    print("Підписники:", artist["followers"]["total"])

    # 2. Пошук треків
    print("\n=== ПОШУК ТРЕКІВ ===")
    search_result = search_tracks(token, "Blinding Lights")

    for item in search_result["tracks"]["items"]:
        print("Трек:", item["name"])
        print("Артист:", item["artists"][0]["name"])
        print("Альбом:", item["album"]["name"])
        print("Популярність:", item["popularity"])
        print("---")

    # 3. Збереження у CSV
    save_to_csv(search_result)



if __name__ == "__main__":
    main()
