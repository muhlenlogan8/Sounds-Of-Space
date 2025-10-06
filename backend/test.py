import requests
import json

NASA_URL = "https://images-api.nasa.gov"

def fetchImage(search):
    url = f"{NASA_URL}/search?q={search}&media_type=image"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # with open("nasa_data.json", "w") as f:
        #     json.dump(data, f, indent=4)
        for i in range(5):
            print(data["collection"]["items"][i]["links"][0]["href"])
        
fetchImage("nebula")