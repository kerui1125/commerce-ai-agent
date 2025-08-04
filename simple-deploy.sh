#!/bin/bash

# Commerce AI Agent EC2 Deployment Script
echo "🚀 Starting Commerce AI Agent deployment..."

# Update system packages
echo "📦 Updating system packages..."
sudo yum update -y

# Install Node.js
echo "📦 Installing Node.js..."
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs

# Install Python 3
echo "📦 Installing Python 3..."
sudo yum install -y python3 python3-pip

# Install PM2 for process management
echo "📦 Installing PM2..."
sudo npm install -g pm2

# Navigate to project directory
# Note: Make sure to upload your code to EC2 first
# git clone https://github.com/yourusername/commerce-ai-agent.git
cd commerce-ai-agent

# Setup backend
echo "🔧 Setting up backend..."
cd backend
pip3 install -r requirements.txt

# Get OpenAI API key from user
read -p "Enter your OpenAI API key: " OPENAI_API_KEY
echo "OPENAI_API_KEY=$OPENAI_API_KEY" > .env

# Start backend service
echo "🚀 Starting backend service..."
pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000" --name backend

# Setup frontend
echo "🔧 Setting up frontend..."
cd ../frontend
npm install
npm run build

# Start frontend service
echo "🚀 Starting frontend service..."
pm2 start "npx serve -s build -l 3000" --name frontend

# Save PM2 configuration
pm2 save
pm2 startup

# Get public IP address
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

echo "✅ Deployment completed successfully!"
echo "🌐 Frontend: http://$PUBLIC_IP:3000"
echo "🔧 Backend API: http://$PUBLIC_IP:8000"
echo "📚 API Documentation: http://$PUBLIC_IP:8000/docs"

echo ""
echo "📊 Useful commands:"
echo "  Check status: pm2 status"
echo "  View logs: pm2 logs"
echo "  Restart services: pm2 restart all"
echo "  Stop services: pm2 stop all"