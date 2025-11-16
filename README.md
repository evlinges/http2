# Лабораторна робота №2  
## Розробка простого HTTP-клієнта  
### Використання Spotify Web API

---

## 1. Мета роботи

Ознайомитися з принципами роботи HTTP-клієнтів, виконанням HTTP-запитів методами GET і POST,  
та реалізувати клієнт для взаємодії з публічним REST API.  
Отримати практичні навички роботи з OAuth 2.0 Client Credentials Flow та обробкою JSON-даних.

---

## 2. Опис API

### 2.1. Spotify Web API

Spotify Web API — це REST API, що дозволяє отримувати дані про артистів, треки, альбоми, плейлисти,  
а також здійснювати пошук музики.

Документація:  
https://developer.spotify.com/documentation/web-api

### 2.2. Реєстрація застосунку

Для доступу до API був створений застосунок **Lab2HTTPClient** у Spotify Developer Dashboard.  
Було зазначено:

- Website: `https://example.com`
- Redirect URI: `http://127.0.0.1:8000/callback`
- App Status: Development mode
- API used: Web API

Після створення були згенеровані **Client ID** та **Client Secret**.

### 2.3. Скриншот налаштувань застосунку

![dashboard](./screenshots/Screenshot_from_2025-11-16_14-15-35.png)

---

## 3. Реалізація авторизації (OAuth 2.0 Client Credentials Flow)

Для доступу до Spotify Web API виконується POST-запит:

```
https://accounts.spotify.com/api/token
```

Заголовок:

```
Authorization: Basic base64(CLIENT_ID:CLIENT_SECRET)
```

Тіло:

```
grant_type=client_credentials
```

### 3.1. Код отримання access-token

```python
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
```

### 3.2. Результат отримання токена

![token](./screenshots/Screenshot_from_2025-11-16_14-16-09.png)

---

## 4. GET-запит №1 — отримання інформації про артиста

Було виконано запит:

```
GET https://api.spotify.com/v1/artists/1Xyo4u8uXC1ZmMpatF05PJ
```

(артист — **The Weeknd**)

### 4.1. Код запиту

```python
def get_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()
```

### 4.2. Результат виконання

![artist](./screenshots/Screenshot_from_2025-11-16_14-19-28.png)

---

## 5. GET-запит №2 — пошук треків

Ендпоїнт пошуку:

```
https://api.spotify.com/v1/search
```

Параметри:

```
q=Blinding Lights
type=track
limit=5
```

### 5.1. Код пошуку

```python
def search_tracks(token, query):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": 5}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
```

### 5.2. Результати пошуку

![search](./screenshots/Screenshot_from_2025-11-16_14-27-16.png)

---

## 6. Збереження даних у CSV

Було збережено список знайдених треків у файл **tracks.csv** з полями:

- track_name  
- artist  
- album  
- popularity  

### 6.1. Код збереження

```python
def save_to_csv(search_result, filename="tracks.csv"):
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
    print(f"CSV-файл '{filename}' успішно створено!")
```

---

## 7. Висновки

У ході виконання лабораторної роботи було створено повноцінний HTTP-клієнт для взаємодії зі Spotify Web API.  

Було реалізовано:

- авторизацію через OAuth 2.0 Client Credentials  
- отримання access token  
- GET-запит до ендпоїнта артиста  
- GET-запит для пошуку треків  
- збереження отриманих результатів у CSV  

Практично закріплено навички роботи з HTTP-протоколом, REST API, JSON, а також обробкою та збереженням даних у Python.

---
