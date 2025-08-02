#!/usr/bin/env python3
"""
Simple script to run the PDF Document Translator web application.
"""

if __name__ == '__main__':
    from app import app
    print("🚀 Starting PDF Document Translator...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🌍 Ready to translate your PDF documents!")
    print("-" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)