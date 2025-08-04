from pydantic import BaseModel
from typing import Optional, List

class Rating(BaseModel):
    rate: float
    count: int
    
class Product(BaseModel):
    id: int
    title: str
    price: float
    description: str
    category: str
    image: str
    rating: Rating
    tags: Optional[List[str]] = []

class ChatRequest(BaseModel):
    message: str
    type: str  # "general_conversation", "product_recommendation_text", "product_search_image"
    image: Optional[str] = None  # base64 encoded image

class ChatResponse(BaseModel):
    response: str
    products: Optional[List[Product]] = []
