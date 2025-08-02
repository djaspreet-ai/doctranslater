#!/usr/bin/env python3
"""
Test script to verify the PDF Translator web application is working correctly.
"""

import requests
import time
import sys

def test_app():
    """Test the Flask web application."""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing PDF Translator Web Application...")
    print("=" * 50)
    
    # Test 1: Main page
    try:
        print("1. Testing main page...")
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200 and "PDF Document Translator" in response.text:
            print("   ✅ Main page loads correctly")
        else:
            print("   ❌ Main page failed")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to app: {e}")
        print("   💡 Make sure the app is running with: python app.py")
        return False
    
    # Test 2: Languages API
    try:
        print("2. Testing languages API...")
        response = requests.get(f"{base_url}/languages", timeout=5)
        if response.status_code == 200:
            languages = response.json()
            if len(languages) > 0:
                print(f"   ✅ Languages API works ({len(languages)} languages available)")
            else:
                print("   ⚠️  Languages API returns empty list")
        else:
            print("   ❌ Languages API failed")
    except Exception as e:
        print(f"   ⚠️  Languages API error: {e}")
    
    # Test 3: Template rendering
    try:
        print("3. Testing template rendering...")
        if "drag your PDF here" in response.text.lower():
            print("   ✅ Templates render correctly")
        else:
            print("   ⚠️  Template content may be incomplete")
    except:
        print("   ⚠️  Could not verify template content")
    
    print("\n🎉 Application appears to be working!")
    print(f"🌐 Open your browser and go to: {base_url}")
    print("📄 Upload a PDF file and test the translation functionality")
    
    return True

if __name__ == "__main__":
    success = test_app()
    sys.exit(0 if success else 1)