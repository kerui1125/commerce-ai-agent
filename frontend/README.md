# Commerce AI Agent - Frontend

React TypeScript frontend for the Commerce AI Agent - a conversational AI interface for e-commerce product recommendations and search.

## Features

- Responsive Chat Interface: Works on desktop, tablet, and mobile
- Three Conversation Types:
  - General conversation with AI
  - Text-based product recommendations
  - Image-based product search
- Real-time Messaging: Auto-scroll to latest messages
- Image Upload: Drag & drop or click to upload images
- Product Display: Beautiful product cards with images and details
- Professional UI: Built with AWS Cloudscape Design System

## Tech Stack

- React 18: Modern React with hooks
- TypeScript: Type-safe development
- AWS Cloudscape: Professional UI components
- Axios: HTTP client for API calls
- Vite: Fast build tool

## Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn

### Local Development
```bash
# Install dependencies
npm install

# Start development server
npm start
```

The app will open at `http://localhost:3000`

### Environment Setup
The frontend connects to the backend at `http://localhost:8000` by default. For production, update the API URL in the code.

## Usage

1. Select Conversation Type: Choose from the dropdown
   - General Conversation: Chat with the AI
   - Product Recommendation: Ask for product suggestions
   - Image Search: Upload images to find similar products

2. Send Messages: Type in the input field and press Enter or click Send

3. Upload Images: When in Image Search mode, upload images using the file picker

4. View Results: Product recommendations appear as cards below messages

## Build & Deploy

### Production Build
```bash
npm run build
```

### Production Deployment
```bash
# Build for production
npm run build

# Serve with static server
npx serve -s build -l 3000
```

## Architecture

```
frontend/
├── public/             # Static assets
├── src/
│   ├── components/
│   │   └── SimpleChat.tsx    # Main chat component
│   ├── App.tsx              # App layout
│   ├── index.tsx            # Entry point
│   └── index.css            # Global styles
├── package.json
└── README.md
```

## Features Detail

### Chat Interface
- Full-screen layout that adapts to all screen sizes
- Fixed header and controls with scrollable message area
- Auto-scroll to latest messages
- Loading states with visual feedback

### Message Types
- User messages: Right-aligned with blue background
- AI responses: Left-aligned with gray background
- Image previews: Uploaded images shown in chat
- Product cards: Rich product information display

### Responsive Design
- Desktop: 3-column product layout
- Tablet: 2-column product layout  
- Mobile: Single-column layout
- Touch-friendly controls and interactions

## API Integration

The frontend communicates with the backend via REST API:

```typescript
// Chat request
POST /api/chat
{
  message: string,
  type: 'general_conversation' | 'product_recommendation_text' | 'product_search_image',
  image?: string // base64 encoded
}
```

## Deployment

### Production Considerations
- Static file serving for SPA routing
- Gzip compression for faster loading
- Security headers for protection
- Health checks for monitoring
- Static asset caching for performance

### Suitable Platforms
- AWS S3 + CloudFront
- Netlify
- Vercel
- Any static hosting service

## Performance

- Code splitting for faster initial load
- Image optimization for uploaded files
- Efficient re-renders with React best practices
- Responsive images for different screen sizes