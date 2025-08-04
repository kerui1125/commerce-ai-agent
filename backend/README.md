# Commerce AI Agent - Backend

FastAPI backend service for the Commerce AI Agent that provides conversational AI capabilities for e-commerce product recommendations and search.

## Features

- General Conversation: Chat with the AI assistant
- Text-based Product Recommendation: Get product suggestions from text queries
- Image-based Product Search: Upload images to find similar products
- Local Product Data: Fast product lookup with pre-generated tags
- OpenAI Integration: Powered by GPT-4o for intelligent responses

## Tech Stack

- FastAPI: Modern Python web framework  
- OpenAI API: For AI conversations and image analysis
- Pydantic: Data validation and serialization

## API Endpoints

### POST /api/chat
Main chat endpoint that handles all conversation types.

**Request Body:**
```json
{
  "message": "Hello, what can you do?",
  "type": "general_conversation|product_recommendation_text|product_search_image",
  "image": "base64_encoded_image_data_or_null"
}
```

**Response:**
```json
{
  "response": "AI response text",
  "products": [
    {
      "id": 1,
      "title": "Product Name",
      "price": 29.99,
      "description": "Product description",
      "category": "clothing",
      "image": "https://example.com/image.jpg",
      "rating": {"rate": 4.5, "count": 100},
      "tags": ["tag1", "tag2"]
    }
  ]
}
```

### GET /health
Health check endpoint.

### GET /
API information and status.

## Setup

### Environment Variables
Create a `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Local Development
```bash
# activate virtual env
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

## Data

The application uses local product data stored in `app/data/products.json` for fast performance. This data includes:
- Product information from Fake Store API: https://fakestoreapi.com/products
- AI-generated tags for each product
- Pre-processed data for quick search

## Architecture

```
backend/
├── app/
│   ├── data/           # Product data
│   ├── models/         # Pydantic models
│   ├── services/       # Business logic
│   │   ├── chat_service.py      # Main chat logic
│   │   ├── product_service.py   # Product operations
│   │   ├── openai_service.py    # OpenAI integration
│   │   └── data_fetcher.py      # Data preparation
│   └── main.py         # FastAPI app
├── requirements.txt
└── Dockerfile
```

## Deployment

Suitable for deployment on:
- AWS EC2 (t2.micro or larger)
- Railway, Render, Heroku
- Any Python hosting platform

## Performance

- Local data storage for fast product lookup
- Async operations for concurrent request handling
- Caching of product data in memory
- Health checks for monitoring