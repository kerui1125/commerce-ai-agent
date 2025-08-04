Design Doc

1. Business Requirement:
a. Users are able to use the AI agent to do general conversation
b. Users are able to use the AI agent to get text based product recommandation
c. Users are able to use the AI agent to do image-based product search

2. System Architecture:
a. Backend: Python + FastAPI (Python is the coding language i most familiar with, FastAPI is fast for small-mid size project development). Development Environment: Venv
b. Frontend: React
https://github.com/cloudscape-design/demos/tree/main/src/pages/chat

c. Pipeline: Github Actions (This whole repo will be deployed on Github)
d. Deploy: Docker
e. Database: Docker mysql (Relational DB is suitable at this situation since I am building the MVP with <100 product info.Also this db  I am most familiar with)

3. API Design
POST /api/chat
The agent will look at the "type" field in the request body to decide how to process the request.
a. 
body: {
  "message": "Hello, what can you do?",
  "type": "general_conversation",
  "image": null
}

b.
body {
    "message": "Recommend me a t-shirt for sports.",
    "type": "product_recommendation_text",
    "image": null
}

c. 
body {
  "message": "Find something like this",
  "type": "product_search_image", 
  "image": "base64_encoded_image_data"
}

4. Entity
a. user
b. product table {
    id,
    name,          # "Nike Dri-FIT Sports T-Shirt"
    description,   # "Red Nike athletic t-shirt for sports and running"
    image_url,     # "https://example.com/tshirt.jpg"
    price,
    category,      # "clothing"
    tags           # "sports,athletic,breathable,red,nike,t-shirt"
}
Product table link: https://fakestoreapi.com/products
Use OpenAI GPT4o to generate "tags" then save to the db table.

5. Deep dive:
a. OpenAI GPT4o to handle general communications ?reference?
b. OpenAI GPT4o to handle text based recommandations ?reference?
c. OpenAI Vision API analyzes the image
