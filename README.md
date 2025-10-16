# Visual Product Matcher

A Flask-based web application that uses computer vision to find visually similar products based on uploaded images. Built with TensorFlow, FAISS, and Bootstrap for a modern, responsive user experience.

##  Features

- **Dual Input Methods**: Upload images directly or provide image URLs
- **Visual Similarity Search**: Find similar products using deep learning features
- **Interactive Filtering**: Filter results by similarity score threshold
- **Mobile Responsive**: Optimized for all device sizes
- **Real-time Results**: Instant visual feedback with loading states
- **Product Database**: 100+ products across 5 categories (jeans, sneakers, sunglasses, t-shirts, watches)

##  Technical Approach

The application uses a **MobileNet-based feature extraction pipeline**:

1. **Feature Extraction**: MobileNet (pre-trained on ImageNet) extracts 1024-dimensional feature vectors
2. **Vector Indexing**: FAISS creates an efficient similarity search index
3. **Real-time Search**: Uploaded images are processed and compared against the indexed database
4. **Similarity Scoring**: Cosine similarity between feature vectors determines product matches

**Key Technologies**: TensorFlow, FAISS, Flask, Bootstrap, jQuery

##  Quick Start

### Local Development

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**

   ```bash
   python start_server.py
   ```

3. **Open your browser:**
   Navigate to `http://localhost:5000`


##  Usage

1. **Upload an Image**: Choose a file or paste an image URL
2. **View Results**: See your uploaded image and similar products
3. **Filter Results**: Use the similarity slider to refine results
4. **Explore Products**: Click on product cards to see details

##  Project Structure

```
visual-product-matcher/
├── backend/
│   ├── app.py              # Flask application & API endpoints
│   └── feature_extractor.py # MobileNet feature extraction
├── static/
│   ├── images/             # Product database (100+ images)
│   │   ├── jeans/          # Jeans category
│   │   ├── sneakers/       # Sneakers category
│   │   ├── sunglasses/     # Sunglasses category
│   │   ├── t-shirt/        # T-shirts category
│   │   └── watch/          # Watches category
│   ├── script.js           # Frontend JavaScript & filtering
│   └── style.css           # Responsive CSS styling
├── templates/
│   └── index.html          # Main HTML template
├── products.json           # Product metadata (100 products)
├── product_ids.json        # FAISS index mapping
├── product.index           # Pre-built FAISS index
├── requirements.txt        # Python dependencies
├── runtime.txt            # Python version specification
└── README.md              # This file
```

## API Reference

### Endpoints

- `GET /` - Main application page
- `POST /api/search` - Search for similar products

### Search API

**Request:**

- `file`: Image file (multipart/form-data)
- `url`: Image URL (form data)

**Response:**

```json
{
  "results": [
    {
      "name": "Product Name",
      "category": "jeans",
      "image_url": "static/images/jeans/product.jpg",
      "similarity": 0.85
    }
  ]
}
```


