
import os
import json

products = []
image_dir = "static/images"

for category in os.listdir(image_dir):
    category_dir = os.path.join(image_dir, category)
    if os.path.isdir(category_dir):
        for image_file in os.listdir(category_dir):
            product = {
                "id": f"{category}-{os.path.splitext(image_file)[0]}",
                "name": image_file.split('.')[0].replace('-', ' ').title(),
                "category": category,
                "image_path": os.path.join(category_dir, image_file)
            }
            products.append(product)

with open("products.json", "w") as f:
    json.dump(products, f, indent=4)
