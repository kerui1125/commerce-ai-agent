from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from .models import ChatRequest, ChatResponse
from .services.chat_service import process_chat
import httpx
import io

app = FastAPI(
    title="Commerce AI Agent",
    description="An AI-powered agent for e-commerce product recommendations and search",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
        """Welcome endpoint"""
        return {
        "message": "Commerce AI Agent API is running!",
        "endpoints": {
            "chat": "/api/chat",
            "docs": "/docs",
            "health": "/health"
        }
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint that handles all three types of interactions:
    
    - general_conversation: Regular chat with the AI
    - product_recommendation_text: Text-based product search  
    - product_search_image: Image-based product search
    
    Example requests:
    {
        "message": "Hello, what can you do?",
        "type": "general_conversation",
        "image": null
    },
    {
        "message": "Recommend me a t-shirt for sports.",
        "type": "product_recommendation_text",
        "image": null
    },
    {
        "message": "Find something like this",
        "type": "product_search_image", 
        "image": "base64_encoded_image_data"
    }
    """
    return await process_chat(request)


@app.get("/api/proxy-image")
async def proxy_image(url: str):
    """
    Proxy endpoint to fetch images from external sources and bypass CORS/referrer restrictions
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Referer": "https://fakestoreapi.com/"
                }
            )
            if response.status_code == 200:
                return StreamingResponse(
                    io.BytesIO(response.content),
                    media_type=response.headers.get("content-type", "image/jpeg")
                )
            else:
                # Return a placeholder if image fails to load
                return {"error": "Image not found"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Commerce AI Agent"}
