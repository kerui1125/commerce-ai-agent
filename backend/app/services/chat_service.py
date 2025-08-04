from ..models import ChatRequest, ChatResponse, Product
from .product_service import fetch_products
from .openai_service import generate_product_tags
from typing import List
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def process_chat(request: ChatRequest) -> ChatResponse:
    if request.type == "general_conversation":
        return await handle_general_conversation(request.message)
    elif request.type == "product_recommendation_text":
        return await handle_text_recommendation(request.message)
    elif request.type == "product_search_image":
        return await handle_image_search(request.message, request.image)
    else:
        return ChatResponse(response="I don't understand that request type.", products=[])


async def handle_general_conversation(message: str) -> ChatResponse:
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant for an e-commerce website. Be friendly and helpful."
                },
                {
                    "role": "user", 
                    "content": message
                    },
            ]
        )
        return ChatResponse(response=completion.choices[0].message.content, products=[])
    except Exception as e:
        return ChatResponse(response=f"Sorry, I had an error: {e}", products=[])


async def handle_text_recommendation(message: str) -> ChatResponse:
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """
                    Extract 3-5 search keywords from the user's product request. 
                    Return only the keywords separated by commas, no other text."
                    """
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )
        search_tags = [tag.strip() for tag in completion.choices[0].message.content.split(",")]
        all_products = await fetch_products()
        matching_products = []
        for product in all_products:
            match_count = 0
            for search_tag in search_tags:
                found_match = False
                for product_tag in product.tags:
                    if search_tag.lower() in product_tag.lower():
                        found_match = True
                        break
                if found_match:
                    match_count += 1
            if match_count > 0:
                matching_products.append((product, match_count))
        matching_products.sort(key=lambda x: x[1], reverse=True)
        top_products = [product for product, _ in matching_products[:3]]
        
        if top_products:
            response_text = f"I found {len(top_products)} products that match your request!"
        else:
            response_text = "Sorry, I couldn't find any matching products."
            
        return ChatResponse(response=response_text, products=top_products)
    
    except Exception as e:
        return ChatResponse(response=f"Sorry, I had an error: {e}", products=[])


async def handle_image_search(message: str, image: str) -> ChatResponse:
    try:
        if image.startswith("http"):
            image_content = {"url": image}
        else:
            image_content = {"url": f"data:image/jpeg;base64,{image}"}

        response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": """
                        Analyze this image and extract 3-5 product search keywords that describe what you see. 
                        Return only the keywords separated by commas, no other text.
                        """
                    },
                    {
                        "type": "image_url",
                        "image_url": image_content
                    },
                ],
            }
        ],
        max_tokens=300,
        )
        search_tags = [tag.strip() for tag in response.choices[0].message.content.split(",")]
        all_products = await fetch_products()
        matching_products = []
        for product in all_products:
            match_count = 0
            for search_tag in search_tags:
                found_match = False
                for product_tag in product.tags:
                    if search_tag.lower() in product_tag.lower():
                        found_match = True
                        break
                if found_match:
                    match_count += 1
            if match_count > 0:
                matching_products.append((product, match_count))
        matching_products.sort(key=lambda x: x[1], reverse=True)
        top_products = [product for product, _ in matching_products[:3]]
        
        if top_products:
            response_text = f"I found {len(top_products)} products that match your request!"
        else:
            response_text = "Sorry, I couldn't find any matching products."
            
        return ChatResponse(response=response_text, products=top_products)
    
    except Exception as e:
        return ChatResponse(response=f"Sorry, I had an error: {e}", products=[])


if __name__ == "__main__":
    import asyncio
    
    async def test():
        # # Test 1: General conversation
        # print("=== Testing General Conversation ===")
        # request1 = ChatRequest(
        #     message="Hello, what can you do?",
        #     type="general_conversation",
        #     image=None
        # )
        # response1 = await process_chat(request1)
        # print(f"Response: {response1.response}")
        # print(f"Products: {len(response1.products)}")
        
        # # Test 2: Product recommendation
        # print("\n=== Testing Product Recommendation ===")
        # request2 = ChatRequest(
        #     message="I need a t-shirt for sports",
        #     type="product_recommendation_text", 
        #     image=None
        # )
        # response2 = await process_chat(request2)
        # print(f"Response: {response2.response}")
        # print(f"Products found: {len(response2.products)}")
        # if response2.products:
        #     print(f"First product: {response2.products[0].title}")
        #     print(f"First product tags: {response2.products[0].tags}")
        print("\n=== Testing Image Search ===")
        request3 = ChatRequest(
            message="Find products like this",
            type="product_search_image",
            image="https://fakestoreapi.com/img/71-3HjGNDUL._AC_SY879._SX._UX._SY._UY_.jpg"
        )
        response3 = await process_chat(request3)
        print(f"Response: {response3.response}")
        print(f"Products found: {len(response3.products)}")
        if response3.products:
            print(f"First product: {response3.products[0].title}")
            print(f"First product tags: {response3.products[0].tags}")
    asyncio.run(test())
