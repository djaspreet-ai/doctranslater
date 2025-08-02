#!/usr/bin/env python3
"""
PDF Document Translator Web Application
A Flask web app that translates PDF documents using LibreTranslate while preserving formatting.
"""

import os
import sys
import re
import json
import traceback
from pathlib import Path
from typing import List, Dict, Optional
import tempfile
import uuid
from datetime import datetime

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io
import requests
from langdetect import detect, DetectorFactory
# Note: Using direct API calls instead of libretranslatepy for better compatibility
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename

# Set seed for consistent language detection
DetectorFactory.seed = 0

app = Flask(__name__)
app.secret_key = 'pdf-translator-secret-key-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

class PDFTranslator:
    """Main PDF translation class using LibreTranslate."""
    
    def __init__(self, libretranslate_url: str = "https://libretranslate.com"):
        """Initialize the translator with LibreTranslate API."""
        self.api_url = libretranslate_url
        # Using direct API calls for better compatibility
        self.supported_languages = self._get_supported_languages()
        
    def _get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages from LibreTranslate."""
        try:
            # Try to get languages using a direct request
            response = requests.get(f"{self.api_url}/languages")
            if response.status_code == 200:
                languages = response.json()
                return {lang['code']: lang['name'] for lang in languages}
            else:
                raise Exception(f"HTTP {response.status_code}")
        except Exception as e:
            print(f"Error fetching supported languages: {e}")
            # Fallback to common languages
            return {
                'en': 'English',
                'es': 'Spanish',
                'fr': 'French',
                'de': 'German',
                'it': 'Italian',
                'pt': 'Portuguese',
                'ru': 'Russian',
                'ja': 'Japanese',
                'ko': 'Korean',
                'zh': 'Chinese',
                'ar': 'Arabic',
                'hi': 'Hindi',
                'nl': 'Dutch',
                'sv': 'Swedish',
                'da': 'Danish',
                'no': 'Norwegian',
                'fi': 'Finnish',
                'pl': 'Polish',
                'cs': 'Czech',
                'hu': 'Hungarian',
                'tr': 'Turkish'
            }
    
    def detect_language(self, text: str) -> str:
        """Detect the language of the given text."""
        try:
            # Clean text for better detection
            cleaned_text = re.sub(r'[^\w\s]', ' ', text[:1000])
            detected = detect(cleaned_text)
            return detected
        except Exception:
            return 'en'  # Default to English if detection fails
    
    def extract_text_with_formatting(self, pdf_path: str) -> List[Dict]:
        """Extract text from PDF using PyPDF2."""
        pages_content = []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                # Since PyPDF2 doesn't preserve detailed formatting,
                # we'll split text into lines and create simple structure
                lines = text.split('\n')
                page_content = {
                    'page_num': page_num,
                    'blocks': []
                }
                
                if lines:
                    block_content = {
                        'lines': []
                    }
                    
                    for line_text in lines:
                        if line_text.strip():  # Only add non-empty lines
                            block_content['lines'].append({
                                'text': line_text.strip(),
                                'formatting': [{'text': line_text.strip(), 'size': 12}]  # Default formatting
                            })
                    
                    if block_content['lines']:
                        page_content['blocks'].append(block_content)
                
                pages_content.append(page_content)
        
        return pages_content
    
    def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text using LibreTranslate API directly."""
        try:
            if not text.strip():
                return text
            
            # Split long text into chunks to avoid API limits
            max_chars = 4000
            if len(text) <= max_chars:
                return self._call_translate_api(text, source_lang, target_lang)
            
            # Split into sentences and translate in chunks
            sentences = re.split(r'(?<=[.!?])\s+', text)
            translated_chunks = []
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk + sentence) <= max_chars:
                    current_chunk += sentence + " "
                else:
                    if current_chunk:
                        translated = self._call_translate_api(current_chunk.strip(), source_lang, target_lang)
                        translated_chunks.append(translated)
                    current_chunk = sentence + " "
            
            # Translate remaining chunk
            if current_chunk:
                translated = self._call_translate_api(current_chunk.strip(), source_lang, target_lang)
                translated_chunks.append(translated)
            
            return " ".join(translated_chunks)
            
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Return original text if translation fails
    
    def _call_translate_api(self, text: str, source_lang: str, target_lang: str) -> str:
        """Make direct API call to LibreTranslate."""
        try:
            response = requests.post(f"{self.api_url}/translate", json={
                'q': text,
                'source': source_lang,
                'target': target_lang,
                'format': 'text'
            })
            
            if response.status_code == 200:
                result = response.json()
                return result.get('translatedText', text)
            else:
                print(f"Translation API error: {response.status_code}")
                return text
        except Exception as e:
            print(f"Translation API call error: {e}")
            return text
    
    def create_translated_pdf(self, original_content: List[Dict], translated_content: List[Dict], 
                            output_path: str) -> None:
        """Create a new PDF with translated content using ReportLab."""
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        for page_data, translated_page in zip(original_content, translated_content):
            # Add page break between pages (except for first page)
            if page_data['page_num'] > 0:
                story.append(Paragraph("<br/><br/>--- Page Break ---<br/><br/>", styles['Normal']))
            
            for block in translated_page['blocks']:
                for line in block['lines']:
                    if line['text'].strip():
                        # Create paragraph with translated text
                        para = Paragraph(line['text'], styles['Normal'])
                        story.append(para)
        
        doc.build(story)
    
    def translate_pdf(self, input_path: str, target_lang: str, output_path: str = None) -> Dict:
        """Main method to translate a PDF document."""
        result = {
            'success': False,
            'message': '',
            'source_language': '',
            'target_language': '',
            'output_file': ''
        }
        
        try:
            if not os.path.exists(input_path):
                result['message'] = f"File {input_path} not found"
                return result
            
            if target_lang not in self.supported_languages:
                result['message'] = f"Language '{target_lang}' not supported"
                return result
            
            # Generate output path if not provided
            if not output_path:
                input_file = Path(input_path)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(
                    app.config['OUTPUT_FOLDER'], 
                    f"{input_file.stem}_{target_lang}_{timestamp}.pdf"
                )
            
            # Extract text
            pages_content = self.extract_text_with_formatting(input_path)
            
            # Detect source language
            all_text = ""
            for page in pages_content:
                for block in page['blocks']:
                    for line in block['lines']:
                        all_text += line['text'] + " "
            
            source_lang = self.detect_language(all_text)
            result['source_language'] = self.supported_languages.get(source_lang, source_lang)
            result['target_language'] = self.supported_languages[target_lang]
            
            # Translate content
            translated_pages = []
            
            for page_idx, page_content in enumerate(pages_content):
                translated_page = {
                    'page_num': page_content['page_num'],
                    'blocks': []
                }
                
                for block in page_content['blocks']:
                    translated_block = {'lines': []}
                    
                    for line in block['lines']:
                        translated_text = self.translate_text(
                            line['text'], source_lang, target_lang
                        )
                        translated_block['lines'].append({
                            'text': translated_text
                        })
                    
                    translated_page['blocks'].append(translated_block)
                
                translated_pages.append(translated_page)
            
            # Create new PDF
            self.create_translated_pdf(pages_content, translated_pages, output_path)
            
            result['success'] = True
            result['message'] = 'Translation completed successfully'
            result['output_file'] = output_path
            
        except Exception as e:
            result['message'] = f"Error during translation: {str(e)}"
            print(f"Translation error: {traceback.format_exc()}")
        
        return result

# Initialize translator
translator = PDFTranslator()

@app.route('/')
def index():
    """Main page with upload form."""
    return render_template('index.html', languages=translator.supported_languages)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and translation."""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file selected'})
    
    file = request.files['file']
    target_lang = request.form.get('target_language')
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'})
    
    if not target_lang:
        return jsonify({'success': False, 'message': 'No target language selected'})
    
    if file and file.filename.lower().endswith('.pdf'):
        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Translate the PDF
        result = translator.translate_pdf(filepath, target_lang)
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        if result['success']:
            # Return download link
            output_filename = os.path.basename(result['output_file'])
            result['download_url'] = f'/download/{output_filename}'
        
        return jsonify(result)
    
    return jsonify({'success': False, 'message': 'Please upload a PDF file'})

@app.route('/download/<filename>')
def download_file(filename):
    """Download translated file."""
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True, download_name=filename)
        else:
            return "File not found", 404
    except Exception as e:
        return f"Error downloading file: {str(e)}", 500

@app.route('/languages')
def get_languages():
    """API endpoint to get supported languages."""
    return jsonify(translator.supported_languages)

@app.errorhandler(413)
def too_large(e):
    return jsonify({'success': False, 'message': 'File too large. Maximum size is 16MB.'}), 413

def main():
    """Entry point for the web application."""
    print("🚀 Starting PDF Document Translator Web Application...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("📄 Upload a PDF file and select a target language to translate!")
    print("-" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()