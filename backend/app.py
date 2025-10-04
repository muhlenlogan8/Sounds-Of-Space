from flask import Flask, jsonify
import requests, os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

NASA_API_KEY = os.getenv("NASA_API_KEY")

@app.route("/get-image")
def get_image():
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch image from NASA API"}), 500
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug = True)
