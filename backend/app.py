#app.py

from flask import Flask, request, jsonify, render_template
import os
import json
import numpy as np
import faiss
import requests
import logging
import io
from feature_extractor import get_model, extract_features
from werkzeug.utils import secure_filename



PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Import configuration
import sys
sys.path.append(PROJECT_ROOT)
from config import config

# Get environment
env = os.environ.get('FLASK_ENV', 'development')
app = Flask(__name__, 
           template_folder=os.path.join(PROJECT_ROOT, 'templates'), 
           static_folder=os.path.join(PROJECT_ROOT, 'static'))

# Load configuration
app.config.from_object(config[env])

# Configure logging
logging.basicConfig(
    level=getattr(logging, app.config['LOG_LEVEL']),
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler(app.config['LOG_FILE']),
        logging.StreamHandler()
    ]
)

with open(os.path.join(PROJECT_ROOT, "products.json"), "r") as f:
    products = json.load(f)

with open(os.path.join(PROJECT_ROOT, "product_ids.json"), "r") as f:
    product_ids = json.load(f)
#okay

try:
    faiss_index = faiss.read_index(os.path.join(PROJECT_ROOT, "product.index"))
    model = get_model()
    logging.info("Successfully loaded FAISS index and model")
except Exception as e:
    logging.error(f"Failed to load FAISS index or model: {e}")
    raise

# Ensure upload folder exists
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    logging.info(f"Created upload folder: {UPLOAD_FOLDER}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    """Search for similar products based on uploaded image or URL"""
    try:
        # Validate request
        if 'file' not in request.files and 'url' not in request.form:
            logging.warning("Search request without file or URL")
            return jsonify({"error": "No file or URL provided"}), 400

        filepath = None
        
        # Handle file upload
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            if file and file.filename:
                # Check file extension
                if not file.filename.lower().endswith(tuple(app.config['ALLOWED_EXTENSIONS'])):
                    return jsonify({"error": "Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP"}), 400
                
                # Read image into memory
                img_stream = io.BytesIO(file.read())
                filepath = None # No longer saving to disk
                logging.info(f"File uploaded and read into memory: {file.filename}")
        
        # Handle URL
        elif 'url' in request.form and request.form['url'] != '':
            url = request.form['url']
            try:
                response = requests.get(url, stream=True, timeout=30)
                response.raise_for_status()
                
                # Check content type
                content_type = response.headers.get('content-type', '').lower()
                if not any(ext in content_type for ext in ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']):
                    return jsonify({"error": "URL does not point to a valid image"}), 400
                
                filename = secure_filename(url.split('/')[-1])
                if not filename or '.' not in filename:
                    filename = f"image_{hash(url) % 10000}.jpg"
                
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                logging.info(f"Image downloaded from URL: {url}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Error downloading image from URL {url}: {e}")
                return jsonify({"error": f"Error downloading image: {e}"}), 400
        else:
            return jsonify({"error": "No file or URL provided"}), 400

        # Extract features and search
        try:
            if img_stream is None:
                return jsonify({"error": "Image stream is empty"}), 400

            features = extract_features(img_stream, model)
            D, I = faiss_index.search(np.array([features]), 5)  # Search for 5 most similar products

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

            logging.info(f"Search completed, found {len(results)} results")
            return jsonify({"results": results})

        except Exception as e:
            logging.error(f"Error during feature extraction or search: {e}")
            return jsonify({"error": "Error processing image. Please try a different image."}), 500

    except Exception as e:
        logging.error(f"Unexpected error in search endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Ensure upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Get port from environment (for hosting platforms)
    port = int(os.environ.get('PORT', 5000))
    
    logging.info(f"Starting Visual Product Matcher on port {port}")
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])