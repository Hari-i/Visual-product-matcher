
import json
import numpy as np
import faiss
from backend.feature_extractor import get_model, extract_features

# Load product data
with open("products.json", "r") as f:
    products = json.load(f)

# Load model
model = get_model()

# Extract features and create index
features_list = []
product_ids = []

for product in products:
    try:
        features = extract_features(product["image_path"], model)
        features_list.append(features)
        product_ids.append(product["id"])
    except Exception as e:
        print(f"Error processing {product['image_path']}: {e}")

features_matrix = np.array(features_list, dtype='float32')

# Create FAISS index
index = faiss.IndexFlatL2(features_matrix.shape[1])
index.add(features_matrix)

# Save index and product ids
faiss.write_index(index, "product.index")
with open("product_ids.json", "w") as f:
    json.dump(product_ids, f)
