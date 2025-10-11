from flask import Flask, request, jsonify, render_template
import os
import json
import numpy as np
import faiss
import requests
from feature_extractor import get_model, extract_features
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')), static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static')))

# Load data
with open("../products.json", "r") as f:
    products = json.load(f)

with open("../product_ids.json", "r") as f:
    product_ids = json.load(f)

faiss_index = faiss.read_index("../product.index")
model = get_model()

UPLOAD_FOLDER = '../uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    if 'file' not in request.files and 'url' not in request.form:
        return jsonify({"error": "No file or URL provided"}), 400

    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
    elif 'url' in request.form and request.form['url'] != '':
        url = request.form['url']
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            filename = secure_filename(url.split('/')[-1])
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Error downloading image: {e}"}), 400
    else:
        return jsonify({"error": "No file or URL provided"}), 400

    try:
        features = extract_features(filepath, model)
        D, I = faiss_index.search(np.array([features]), 5) # Search for 5 most similar products

        results = []
        for i in range(len(I[0])):
            product_id = product_ids[I[0][i]]
            product = next((p for p in products if p['id'] == product_id), None)
            if product:
                # Normalize similarity score to 0-1 range (lower distance = higher similarity)
                max_distance = 1000.0  # Approximate maximum distance
                normalized_similarity = max(0, 1 - (D[0][i] / max_distance))
                results.append({
                    "name": product["name"],
                    "category": product["category"],
                    "image_url": product["image_path"],
                    "similarity": float(normalized_similarity)
                })

        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)