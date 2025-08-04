# Commerce AI Agent

A full-stack AI-powered conversational agent for e-commerce product recommendations and search. Built with React TypeScript frontend and FastAPI Python backend.

## 🚀 Live Demo

[Add your deployed URL here]

## ✨ Features

- **💬 General Conversation**: Chat naturally with the AI assistant
- **🔍 Text-based Product Search**: Get recommendations from text queries like "I need a sports t-shirt"
- **📸 Image-based Product Search**: Upload images to find similar products
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **⚡ Real-time Chat**: Auto-scrolling chat interface with loading states
- **🎨 Professional UI**: Built with AWS Cloudscape Design System

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│   React Frontend │ ◄──────────────► │  FastAPI Backend │
│                 │                 │                 │
│ • Chat Interface│                 │ • OpenAI API    │
│ • Image Upload  │                 │ • Product Search│
│ • Product Cards │                 │ • Local Data    │
└─────────────────┘                 └─────────────────┘
```

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **AWS Cloudscape** Design System
- **Axios** for API calls
- **Serve** for production deployment

### Backend
- **FastAPI** with Python 3.11
- **OpenAI GPT-4** for conversations
- **OpenAI Vision API** for image analysis
- **Pydantic** for data validation
- **Local JSON data** for fast product lookup

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API key

### 1. Clone & Setup
```bash
git clone <your-repo>
cd commerce-ai-agent

# Setup backend
cd backend
pip install -r requirements.txt
echo "OPENAI_API_KEY=your_key_here" > .env

# Setup frontend
cd ../frontend
npm install
```

### 2. Run the Application
```bash
# Terminal 1: Start backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Start frontend  
cd frontend
npm start
```

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔧 Development Setup

### Local Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (in another terminal)
cd frontend
npm install
npm start
```

## 📡 API Usage

### Chat Endpoint
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need a sports t-shirt",
    "type": "product_recommendation_text",
    "image": null
  }'
```

### Response Format
```json
{
  "response": "I found 3 products that match your request!",
  "products": [
    {
      "id": 1,
      "title": "Nike Dri-FIT Sports T-Shirt",
      "price": 29.99,
      "description": "Athletic shirt for sports",
      "category": "men's clothing",
      "image": "https://example.com/image.jpg",
      "rating": {"rate": 4.5, "count": 120},
      "tags": ["sports", "athletic", "nike"]
    }
  ]
}
```

## 🚀 Deployment

### AWS EC2 Deployment
1. **Launch EC2 instance** (t2.micro or larger)
2. **Upload your code** to the instance
3. **Run the deployment script**:
   ```bash
   chmod +x simple-deploy.sh
   ./simple-deploy.sh
   ```

### Manual EC2 Setup
```bash
# Install dependencies
sudo yum update -y
sudo yum install python3 python3-pip nodejs npm -y

# Setup backend
cd backend
pip3 install -r requirements.txt
export OPENAI_API_KEY=your_key
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Setup frontend
cd ../frontend
npm install
npm run build
npx serve -s build -l 3000
```

### Other Deployment Options
- **Frontend**: Netlify, Vercel (just upload the build folder)
- **Backend**: Railway, Render, Heroku
- **Full Stack**: DigitalOcean App Platform

## 📊 Performance

- **Local product data** for sub-100ms search responses
- **Async operations** for handling concurrent users
- **Optimized builds** for production
- **Static asset serving** with serve
- **Process management** with PM2

## 🔒 Security

- **Environment variables** for sensitive data
- **CORS configuration** for cross-origin requests
- **Input validation** with Pydantic
- **Process isolation** with PM2
- **Secure deployment** practices

## 📁 Project Structure

```
commerce-ai-agent/
├── backend/
│   ├── app/
│   │   ├── data/products.json      # Product catalog
│   │   ├── models/                 # Pydantic models
│   │   ├── services/               # Business logic
│   │   └── main.py                 # FastAPI app
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/SimpleChat.tsx
│   │   └── App.tsx
│   └── package.json
├── simple-deploy.sh               # EC2 deployment script
└── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Issues**: Create a GitHub issue
- **Documentation**: Check individual README files in backend/ and frontend/
- **API Docs**: Visit http://localhost:8000/docs when running locally

---

Built with ❤️ for modern e-commerce experiences