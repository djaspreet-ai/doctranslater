# PDF Document Translator - Usage Guide

## 🚀 Quick Start

### Option 1: Simple Startup (Recommended)
```bash
# Clone or download the project
cd pdf-document-translator

# Run the startup script (handles everything automatically)
./start.sh
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p uploads outputs

# Start the application
python app.py
```

### Option 3: Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build and run manually
docker build -t pdf-translator .
docker run -p 5000:5000 pdf-translator
```

## 🖥️ Using the Web Interface

### 1. Access the Application
Open your web browser and navigate to:
- **Local development**: http://localhost:5000
- **Docker deployment**: http://localhost:5000

### 2. Upload Your PDF
- **Drag & Drop**: Simply drag your PDF file onto the upload area
- **Browse**: Click the "Choose PDF File" button to select a file
- **File Requirements**: 
  - Format: PDF only
  - Size: Maximum 16MB
  - Content: Text-based PDFs work best

### 3. Select Target Language
- Choose from 20+ supported languages including:
  - English (en), Spanish (es), French (fr)
  - German (de), Italian (it), Portuguese (pt)
  - Russian (ru), Japanese (ja), Korean (ko)
  - Chinese (zh), Arabic (ar), Hindi (hi)
  - And many more...

### 4. Translate
- Click "Translate Document" to start the process
- Wait for the translation to complete (may take 30-60 seconds)
- The system will automatically:
  - Extract text from your PDF
  - Detect the source language
  - Translate to your target language
  - Generate a new PDF with translated content

### 5. Download Results
- Once translation is complete, click "Download Translated PDF"
- The file will be saved with a timestamp and language code
- Example: `document_es_20240115_143052.pdf`

## 🔧 Features & Capabilities

### ✅ What Works Well
- **Text-based PDFs**: Documents with selectable text
- **Simple layouts**: Standard document formats
- **Multiple languages**: 20+ language pairs
- **Batch processing**: Single file at a time
- **Format preservation**: Basic structure maintained

### ⚠️ Limitations
- **Image-based PDFs**: Scanned documents need OCR first
- **Complex layouts**: Tables, forms may lose formatting
- **Large files**: 16MB size limit
- **Translation quality**: Depends on LibreTranslate service

## 🛠️ Configuration

### Environment Variables
```bash
# Custom LibreTranslate instance
export LIBRETRANSLATE_URL="https://your-instance.com"

# File size limit (in bytes)
export MAX_FILE_SIZE="16777216"

# Flask environment
export FLASK_ENV="development"  # or "production"
```

### Custom LibreTranslate Instance
If you want to use your own LibreTranslate instance:

1. **Docker deployment**:
   ```bash
   docker run -ti --rm -p 5001:5000 libretranslate/libretranslate
   ```

2. **Update configuration**:
   ```bash
   export LIBRETRANSLATE_URL="http://localhost:5001"
   ```

3. **Restart the application**

## 📝 Testing

### Test PDF
The application includes a sample PDF (`test_document.pdf`) for testing:
- Contains various text elements
- Multiple sections and formatting
- Perfect for testing translation functionality

### Test Translation
1. Use the provided test PDF
2. Try translating to Spanish (es) or French (fr)
3. Compare original and translated versions

## 🐛 Troubleshooting

### Common Issues

**1. "Error fetching supported languages"**
- Check internet connection
- Verify LibreTranslate service is accessible
- Try restarting the application

**2. "Translation failed"**
- Check if the PDF contains extractable text
- Try with a simpler PDF file
- Verify target language is supported

**3. "File too large"**
- Reduce PDF file size
- Split large documents into smaller files
- Increase MAX_FILE_SIZE if needed

**4. "No text extracted"**
- PDF might be image-based (scanned)
- Try using OCR software first
- Ensure PDF has selectable text

### Performance Tips
- Use text-based PDFs for best results
- Keep files under 10MB for faster processing
- Choose common language pairs for better accuracy
- Test with simple documents first

## 🔒 Security & Privacy

### Data Handling
- **Files are temporary**: Uploaded files are deleted after processing
- **No data storage**: No permanent storage of your documents
- **Secure processing**: Files processed locally or via HTTPS

### Privacy Considerations
- Translation is done via LibreTranslate (external service)
- For sensitive documents, consider running your own LibreTranslate instance
- Files are not permanently stored on our servers

## 📞 Support

### Getting Help
1. Check this usage guide
2. Review the README.md file
3. Check the troubleshooting section
4. Create an issue on GitHub (if applicable)

### Logs and Debugging
- Check terminal output for error messages
- Enable debug mode: `export FLASK_ENV=development`
- Check uploads/ and outputs/ directories for temporary files

---

**Ready to translate your documents? Start with `./start.sh` and open http://localhost:5000!** 🚀