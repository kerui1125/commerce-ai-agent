import json
import os
from typing import List
from ..models import Product, Rating

def load_products_from_file() -> List[Product]:
    """Load products from local JSON file"""
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.json')
    
    try:
        with open(file_path, 'r') as f:
            products_data = json.load(f)
        
        products = []
        for item in products_data:
            rating = Rating(rate=item['rating']['rate'], count=item['rating']['count'])
            product = Product(
                id=item['id'],
                title=item['title'],
                price=item['price'],
                description=item['description'],
                category=item['category'],
                image=item['image'],
                rating=rating,
                tags=item['tags']
            )
            products.append(product)
        
        return products
    except Exception as e:
        print(f"Error loading products from file: {e}")
        return []

# Keep the old function as fallback
async def fetch_products() -> List[Product]:
    """Load products from local file (much faster for deployment)"""
    return load_products_from_file()
