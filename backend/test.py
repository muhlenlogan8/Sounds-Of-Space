import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

NASA_URL = "https://images-api.nasa.gov"

excludeWords = [
    "illustration", "concept", "artist", "diagram", "poster", "chart", "annotated",
    "radar", "arecibo", "goldstone", "infrared", "radio", "false color", "spectrum",
    "black and white", "bw", "grayscale", "composite"
]

def fetchImages(search):
    url = f"{NASA_URL}/search?q={search}&media_type=image"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        items = data["collection"]["items"][:50]
        hrefs = []
        for item in items:
            meta = item["data"][0]
            keywords = [k.lower() for k in meta.get("keywords", [])]
            desc = meta.get("description", "").lower()
            title = meta.get("title", "").lower()
            
            if any(word in desc for word in excludeWords):
                continue
            if any(word in keywords for word in excludeWords):
                continue
            if any(word in title for word in excludeWords):
                continue
            if containsText(item["links"][0]["href"]):
                continue

            hrefs.append(item["links"][0]["href"])
        return jsonify(hrefs)

def containsText(url, threshold = 10):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        text = pytesseract.image_to_string(img)
        return len(text.strip()) >= threshold
    except Exception as e:
        print(f"Error processing image {url}: {e}")
        return False

@app.route("/get-images/<string:search>", methods=["GET"])
def getImages(search):
    return fetchImages(search)

if __name__ == "__main__":
    app.run(debug=True)