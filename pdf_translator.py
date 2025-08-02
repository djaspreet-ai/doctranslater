#!/usr/bin/env python3
"""
PDF Document Translator
Translates PDF documents using LibreTranslate while preserving formatting.
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple

import click
import fitz  # PyMuPDF
import requests
from langdetect import detect, DetectorFactory
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.prompt import Prompt
from libretranslatepy import LibreTranslateAPI

# Set seed for consistent language detection
DetectorFactory.seed = 0

console = Console()

class PDFTranslator:
    """Main PDF translation class using LibreTranslate."""
    
    def __init__(self, libretranslate_url: str = "https://libretranslate.com"):
        """Initialize the translator with LibreTranslate API."""
        self.api_url = libretranslate_url
        self.translator = LibreTranslateAPI(libretranslate_url)
        self.supported_languages = self._get_supported_languages()
        
    def _get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages from LibreTranslate."""
        try:
            languages = self.translator.languages()
            return {lang['code']: lang['name'] for lang in languages}
        except Exception as e:
            console.print(f"[red]Error fetching supported languages: {e}[/red]")
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
                'hi': 'Hindi'
            }
    
    def display_supported_languages(self) -> None:
        """Display supported languages in a formatted table."""
        table = Table(title="Supported Languages")
        table.add_column("Code", style="cyan", no_wrap=True)
        table.add_column("Language", style="magenta")
        
        for code, name in sorted(self.supported_languages.items()):
            table.add_row(code, name)
        
        console.print(table)
    
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
        """Extract text from PDF while preserving basic formatting information."""
        doc = fitz.open(pdf_path)
        pages_content = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Get text blocks with formatting info
            blocks = page.get_text("dict")
            page_content = {
                'page_num': page_num,
                'blocks': []
            }
            
            for block in blocks['blocks']:
                if 'lines' in block:  # Text block
                    block_content = {
                        'bbox': block['bbox'],
                        'lines': []
                    }
                    
                    for line in block['lines']:
                        line_text = ""
                        line_formatting = []
                        
                        for span in line['spans']:
                            line_text += span['text']
                            line_formatting.append({
                                'text': span['text'],
                                'font': span['font'],
                                'size': span['size'],
                                'flags': span['flags'],
                                'color': span['color']
                            })
                        
                        if line_text.strip():  # Only add non-empty lines
                            block_content['lines'].append({
                                'text': line_text,
                                'formatting': line_formatting,
                                'bbox': line['bbox']
                            })
                    
                    if block_content['lines']:
                        page_content['blocks'].append(block_content)
            
            pages_content.append(page_content)
        
        doc.close()
        return pages_content
    
    def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text using LibreTranslate."""
        try:
            if not text.strip():
                return text
            
            # Split long text into chunks to avoid API limits
            max_chars = 4000
            if len(text) <= max_chars:
                translated = self.translator.translate(text, source_lang, target_lang)
                return translated
            
            # Split into sentences and translate in chunks
            sentences = re.split(r'(?<=[.!?])\s+', text)
            translated_chunks = []
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk + sentence) <= max_chars:
                    current_chunk += sentence + " "
                else:
                    if current_chunk:
                        translated = self.translator.translate(current_chunk.strip(), source_lang, target_lang)
                        translated_chunks.append(translated)
                    current_chunk = sentence + " "
            
            # Translate remaining chunk
            if current_chunk:
                translated = self.translator.translate(current_chunk.strip(), source_lang, target_lang)
                translated_chunks.append(translated)
            
            return " ".join(translated_chunks)
            
        except Exception as e:
            console.print(f"[red]Translation error: {e}[/red]")
            return text  # Return original text if translation fails
    
    def create_translated_pdf(self, original_content: List[Dict], translated_content: List[Dict], 
                            output_path: str) -> None:
        """Create a new PDF with translated content preserving formatting."""
        doc = fitz.open()  # Create new PDF
        
        for page_data, translated_page in zip(original_content, translated_content):
            page = doc.new_page(width=595, height=842)  # A4 size
            
            for block_idx, (original_block, translated_block) in enumerate(
                zip(page_data['blocks'], translated_page['blocks'])
            ):
                for line_idx, (original_line, translated_line) in enumerate(
                    zip(original_block['lines'], translated_block['lines'])
                ):
                    # Use original formatting but translated text
                    bbox = original_line['bbox']
                    
                    # Get the primary font info from the first span
                    if original_line['formatting']:
                        font_info = original_line['formatting'][0]
                        font_size = max(8, min(font_info['size'], 16))  # Reasonable size limits
                    else:
                        font_size = 11
                    
                    # Insert translated text
                    try:
                        page.insert_text(
                            (bbox[0], bbox[1] + font_size),
                            translated_line['text'],
                            fontsize=font_size,
                            color=(0, 0, 0)
                        )
                    except Exception:
                        # Fallback if insertion fails
                        page.insert_text(
                            (bbox[0], bbox[1] + 11),
                            translated_line['text'],
                            fontsize=11
                        )
        
        doc.save(output_path)
        doc.close()
    
    def translate_pdf(self, input_path: str, target_lang: str, output_path: str = None) -> bool:
        """Main method to translate a PDF document."""
        if not os.path.exists(input_path):
            console.print(f"[red]Error: File {input_path} not found[/red]")
            return False
        
        if target_lang not in self.supported_languages:
            console.print(f"[red]Error: Language '{target_lang}' not supported[/red]")
            return False
        
        # Generate output path if not provided
        if not output_path:
            input_file = Path(input_path)
            output_path = str(input_file.parent / f"{input_file.stem}_{target_lang}{input_file.suffix}")
        
        console.print(f"[blue]Starting translation to {self.supported_languages[target_lang]}...[/blue]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            
            # Extract text
            task1 = progress.add_task("Extracting text from PDF...", total=None)
            try:
                pages_content = self.extract_text_with_formatting(input_path)
            except Exception as e:
                console.print(f"[red]Error extracting text: {e}[/red]")
                return False
            progress.remove_task(task1)
            
            # Detect source language
            task2 = progress.add_task("Detecting source language...", total=None)
            all_text = ""
            for page in pages_content:
                for block in page['blocks']:
                    for line in block['lines']:
                        all_text += line['text'] + " "
            
            source_lang = self.detect_language(all_text)
            console.print(f"[green]Detected language: {self.supported_languages.get(source_lang, source_lang)}[/green]")
            progress.remove_task(task2)
            
            # Translate content
            task3 = progress.add_task(f"Translating to {self.supported_languages[target_lang]}...", total=len(pages_content))
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
                            'text': translated_text,
                            'bbox': line['bbox']
                        })
                    
                    translated_page['blocks'].append(translated_block)
                
                translated_pages.append(translated_page)
                progress.update(task3, advance=1)
            
            progress.remove_task(task3)
            
            # Create new PDF
            task4 = progress.add_task("Creating translated PDF...", total=None)
            try:
                self.create_translated_pdf(pages_content, translated_pages, output_path)
            except Exception as e:
                console.print(f"[red]Error creating PDF: {e}[/red]")
                return False
            progress.remove_task(task4)
        
        console.print(f"[green]✅ Translation completed! Output saved to: {output_path}[/green]")
        return True


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--target-lang', '-t', help='Target language code (e.g., es, fr, de)')
@click.option('--output', '-o', help='Output file path')
@click.option('--list-languages', '-l', is_flag=True, help='List supported languages')
@click.option('--libretranslate-url', default='https://libretranslate.com', 
              help='LibreTranslate API URL (default: https://libretranslate.com)')
def main(input_file, target_lang, output, list_languages, libretranslate_url):
    """
    PDF Document Translator using LibreTranslate
    
    Translate PDF documents while preserving formatting.
    
    Example usage:
    python pdf_translator.py document.pdf -t es
    python pdf_translator.py document.pdf --target-lang fr --output translated_doc.pdf
    """
    console.print("[bold blue]📄 PDF Document Translator[/bold blue]")
    console.print("Using LibreTranslate for free document translation\n")
    
    # Initialize translator
    try:
        translator = PDFTranslator(libretranslate_url)
    except Exception as e:
        console.print(f"[red]Error initializing translator: {e}[/red]")
        sys.exit(1)
    
    # List languages if requested
    if list_languages:
        translator.display_supported_languages()
        return
    
    # Get target language if not provided
    if not target_lang:
        translator.display_supported_languages()
        target_lang = Prompt.ask("\nEnter target language code")
        
        if target_lang not in translator.supported_languages:
            console.print(f"[red]Invalid language code: {target_lang}[/red]")
            sys.exit(1)
    
    # Perform translation
    success = translator.translate_pdf(input_file, target_lang, output)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()