#!/bin/bash

# Commerce AI Agent EC2 Deployment Script
echo "Starting Commerce AI Agent deployment..."

# Update system packages
echo "Updating system packages..."
sudo yum update -y

# Install Node.js
echo "Installing Node.js..."
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs

# Install Python 3
echo "Installing Python 3..."
sudo yum install -y python3 python3-pip

# Install PM2 for process management
echo "Installing PM2..."
sudo npm install -g pm2

cd commerce-ai-agent

# Setup backend
echo "Setting up backend..."
cd backend
pip3 install -r requirements.txt

# Get OpenAI API key from user
read -p "Enter your OpenAI API key: " OPENAI_API_KEY
echo "OPENAI_API_KEY=$OPENAI_API_KEY" > .env

# Check if backend is already running
if pm2 list | grep -q "backend.*online"; then
    echo "Backend already running, restarting..."
    pm2 restart backend
else
    echo "Starting backend service..."
    pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000" --name backend
fi

# Setup frontend
echo "Setting up frontend..."
cd ../frontend

# Install dependencies with error handling
echo "Installing frontend dependencies..."
npm install --production

# Build with error handling
echo "Building frontend..."
if npm run build; then
    echo "Frontend build successful"
else
    echo "Frontend build failed, exiting..."
    exit 1
fi

# Check if frontend is already running
if pm2 list | grep -q "frontend.*online"; then
    echo "Frontend already running, restarting..."
    pm2 restart frontend
else
    echo "Starting frontend service..."
    pm2 start "npx serve -s build -l 3000" --name frontend
fi

# Save PM2 configuration
pm2 save
pm2 startup

# Get public IP address
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

echo "Deployment completed successfully!"
echo "Frontend: http://$PUBLIC_IP:3000"
echo "Backend API: http://$PUBLIC_IP:8000"
echo "API Documentation: http://$PUBLIC_IP:8000/docs"

echo ""
echo "Useful commands:"
echo "  Check status: pm2 status"
echo "  View logs: pm2 logs"
echo "  Restart services: pm2 restart all"
echo "  Stop services: pm2 stop all"