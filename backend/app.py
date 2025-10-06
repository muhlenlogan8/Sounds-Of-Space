from flask import Flask, jsonify, send_from_directory
import requests, os, random
from dotenv import load_dotenv
from flask_cors import CORS
from datetime import datetime, timedelta
from audio import generate_audio_from_image  # we'll make a helper function

load_dotenv()

app = Flask(__name__, static_folder="static")
CORS(app)

NASA_API_KEY = os.getenv("NASA_API_KEY")
NASA_URL = "https://api.nasa.gov/planetary/apod"

def fetchImage(date, today=False):
    if today:
        url = f"{NASA_URL}?api_key={NASA_API_KEY}"
    else:
        url = f"{NASA_URL}?api_key={NASA_API_KEY}&date={date}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("media_type") == "image":
            # Download the image
            img_url = data["hdurl"] if "hdurl" in data else data["url"]
            img_data = requests.get(img_url).content
            img_path = f"temp_{date}.jpg"
            with open(img_path, "wb") as f:
                f.write(img_data)

            # Generate audio and save to static/audio
            audio_filename = f"{date}.wav"
            audio_path = os.path.join("static/audio", audio_filename)
            generate_audio_from_image(img_path, audio_path)

            # Add audio URL
            data["audio_url"] = f"http://127.0.0.1:5000/audio/{audio_filename}"
            return data
    return None

@app.route("/audio/<filename>")
def get_audio(filename):
    return send_from_directory("static/audio", filename)

@app.route("/get-today")
def get_today():
    today = datetime.now().strftime("%Y-%m-%d")
    data = fetchImage(today, True)
    if data:
        return jsonify(data)
    return jsonify({"error": "No image available for today"}), 404

@app.route("/get-random")
def get_random():
    start = datetime(1995, 6, 16)
    today = datetime.now()
    tries = 0

    while tries < 10:
        randomDays = random.randint(0, (today - start).days)
        randDate = (start + timedelta(days=randomDays)).strftime("%Y-%m-%d")
        data = fetchImage(randDate)
        if data:
            return jsonify(data)
        tries += 1

    return jsonify({"error": "Could not find a random image"}), 500

if __name__ == "__main__":
    os.makedirs("static/audio", exist_ok=True)
    app.run(debug=True)
