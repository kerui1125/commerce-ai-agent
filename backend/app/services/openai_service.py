from openai import OpenAI
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

async def generate_product_tags(title: str, description: str) -> List[str]:
    # Your OpenAI API call here
    # Hint: Use openai.ChatCompletion.create() or the new openai.chat.completions.create()
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": f"""Generate 5-7 search tags for this product. Return only the tags separated by commas, no other text.

                    Product: {title}
                    Description: {description}

                    Example format: red,athletic,t-shirt,sports,nike,clothing"""
                }
            ]
        )
        response_text = completion.choices[0].message.content.strip()
        tags = [tag.strip() for tag in response_text.split(',')]
        return tags

    except Exception as e:
        print(f"Failed to generate product tags using OpenAI, {e}")
        return []

if __name__ == "__main__":
    import asyncio
    
    async def test():
        tags = await generate_product_tags(
            "Nike Dri-FIT T-Shirt", 
            "Athletic shirt for sports and running"
        )
        print(f"Generated tags: {tags}")
    
    asyncio.run(test())
