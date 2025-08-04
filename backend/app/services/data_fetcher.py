import asyncio
import json
import httpx
from .openai_service import generate_product_tags

async def fetch_and_save_products():
    """Fetch products from Fake Store API and save with generated tags"""
    print("Fetching products from Fake Store API...")
    
    async with httpx.AsyncClient() as client:
        response = await client.get("https://fakestoreapi.com/products")
        products_data = response.json()
    
    print(f"Fetched {len(products_data)} products. Generating tags...")
    
    # Generate tags for all products
    enhanced_products = []
    for i, product in enumerate(products_data):
        print(f"Processing product {i+1}/{len(products_data)}: {product['title'][:50]}...")
        
        # Generate tags
        tags = await generate_product_tags(product['title'], product['description'])
        
        # Create enhanced product
        enhanced_product = {
            "id": product['id'],
            "title": product['title'],
            "price": product['price'],
            "description": product['description'],
            "category": product['category'],
            "image": product['image'],
            "rating": {
                "rate": product['rating']['rate'],
                "count": product['rating']['count']
            },
            "tags": tags
        }
        enhanced_products.append(enhanced_product)
    
    # Save to JSON file
    with open('app/data/products.json', 'w') as f:
        json.dump(enhanced_products, f, indent=2)
    
    print(f"Saved {len(enhanced_products)} products with tags to app/data/products.json")

if __name__ == "__main__":
    asyncio.run(fetch_and_save_products())