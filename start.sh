#!/bin/bash

echo "🚀 Starting PDF Document Translator..."
echo "======================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p uploads outputs

# Create test PDF if it doesn't exist
if [ ! -f "test_document.pdf" ]; then
    echo "📄 Creating test PDF..."
    python create_test_pdf.py
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Web Interface: http://localhost:5000"
echo "📁 Test PDF: test_document.pdf"
echo ""
echo "🔧 Features:"
echo "  • Drag & drop PDF upload"
echo "  • 20+ language support"
echo "  • Format preservation"
echo "  • Free translation service"
echo ""
echo "Press Ctrl+C to stop the server"
echo "======================================="
echo ""

# Start the Flask application
python app.py