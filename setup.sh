#!/bin/bash

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Prompt for Groq API key
echo "Please enter your Groq API key (from https://console.groq.com/):"
read api_key

# Create .env file
echo "Creating .env file..."
echo "GROQ_API_KEY=$api_key" > .env

echo "Setup complete! You can now run the application with: streamlit run app.py" 