# PDF Document Translator 🌍

A modern web application that translates PDF documents while preserving their original formatting. Built with Flask and powered by LibreTranslate for free, privacy-focused translation.

## ✨ Features

- **🌐 Multi-language Support**: Translate to/from 20+ languages including English, Spanish, French, German, Chinese, Japanese, Arabic, and more
- **📄 Format Preservation**: Maintains original PDF layout, fonts, and formatting
- **🔒 Privacy First**: Documents are processed securely and automatically deleted after translation
- **💰 Completely Free**: Uses LibreTranslate API - no API keys or costs required
- **📱 Modern UI**: Beautiful, responsive web interface with drag-and-drop file upload
- **⚡ Fast Processing**: Efficient translation with progress indicators
- **🔍 Auto Language Detection**: Automatically detects source document language

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pdf-document-translator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the web interface**
   Open your browser and go to: `http://localhost:5000`

## 🖥️ Usage

1. **Upload PDF**: Drag and drop your PDF file or click to browse (max 16MB)
2. **Select Language**: Choose your target language from the dropdown
3. **Translate**: Click "Translate Document" and wait for processing
4. **Download**: Download your translated PDF with preserved formatting

## 🛠️ Technical Details

### Supported File Formats
- **Input**: PDF files (up to 16MB)
- **Output**: PDF files with translated content

### Translation Engine
- **Service**: LibreTranslate (Open Source)
- **API**: Free public instance at libretranslate.com
- **Fallback**: Comprehensive language list for offline scenarios

### Architecture
- **Backend**: Flask web framework
- **PDF Processing**: PyMuPDF for text extraction and PDF generation
- **Language Detection**: langdetect library
- **Frontend**: Bootstrap 5 with modern CSS and JavaScript
- **File Handling**: Secure upload with automatic cleanup

## 🌍 Supported Languages

| Language | Code | Language | Code |
|----------|------|----------|------|
| English | en | German | de |
| Spanish | es | Italian | it |
| French | fr | Portuguese | pt |
| Russian | ru | Japanese | ja |
| Korean | ko | Chinese | zh |
| Arabic | ar | Hindi | hi |
| Dutch | nl | Swedish | sv |
| Danish | da | Norwegian | no |
| Finnish | fi | Polish | pl |
| Czech | cs | Hungarian | hu |
| Turkish | tr | And more... |

## 📁 Project Structure

```
pdf-document-translator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── setup.py              # Package installation setup
├── templates/            # HTML templates
│   ├── base.html         # Base template with styling
│   └── index.html        # Main page template
├── uploads/              # Temporary file uploads (auto-created)
├── outputs/              # Generated translations (auto-created)
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables

You can customize the application using environment variables:

```bash
export LIBRETRANSLATE_URL="https://your-libretranslate-instance.com"  # Custom LibreTranslate instance
export FLASK_ENV="development"  # Development mode
export MAX_FILE_SIZE="16777216"  # 16MB in bytes
```

### Custom LibreTranslate Instance

To use your own LibreTranslate instance:

1. Install LibreTranslate locally or deploy it
2. Update the URL in `app.py` or set the environment variable
3. Restart the application

## 🐳 Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

Build and run:

```bash
docker build -t pdf-translator .
docker run -p 5000:5000 pdf-translator
```

## 🔒 Security & Privacy

- **No Data Storage**: Files are immediately deleted after processing
- **Secure File Handling**: Validates file types and sizes
- **No API Keys**: Uses free LibreTranslate service
- **Privacy Focused**: No tracking or data collection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LibreTranslate](https://libretranslate.com/) for free translation API
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF processing
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Bootstrap](https://getbootstrap.com/) for the UI components

## 📞 Support

If you encounter any issues or have questions:

1. Check the existing [Issues](https://github.com/your-username/pdf-document-translator/issues)
2. Create a new issue with detailed information
3. Provide sample files (if possible) and error messages

---

**Made with ❤️ for the open source community**
