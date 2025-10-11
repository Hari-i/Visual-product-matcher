
from bing_image_downloader import downloader

queries = ["t-shirt", "jeans", "sneakers", "watch", "sunglasses"]

for query in queries:
    downloader.download(query, limit=10,  output_dir='static/images', adult_filter_off=True, force_replace=False, timeout=60)
