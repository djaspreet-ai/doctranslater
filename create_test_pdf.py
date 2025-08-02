#!/usr/bin/env python3
"""
Script to create a test PDF file for demonstrating the translation functionality.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

def create_test_pdf():
    """Create a simple test PDF with English text."""
    filename = "test_document.pdf"
    
    # Create document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph("Sample Document for Translation", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5*inch))
    
    # Introduction
    intro = Paragraph(
        "This is a sample document created to demonstrate the PDF translation functionality. "
        "The document contains various types of content including headings, paragraphs, and lists.",
        styles['Normal']
    )
    story.append(intro)
    story.append(Spacer(1, 0.3*inch))
    
    # Section 1
    heading1 = Paragraph("About Technology", styles['Heading1'])
    story.append(heading1)
    
    content1 = Paragraph(
        "Technology has revolutionized the way we live, work, and communicate. "
        "From smartphones to artificial intelligence, technological advancements "
        "continue to shape our daily experiences and create new possibilities for the future.",
        styles['Normal']
    )
    story.append(content1)
    story.append(Spacer(1, 0.3*inch))
    
    # Section 2
    heading2 = Paragraph("Environmental Awareness", styles['Heading1'])
    story.append(heading2)
    
    content2 = Paragraph(
        "Climate change is one of the most pressing challenges of our time. "
        "It is important to adopt sustainable practices, reduce carbon emissions, "
        "and protect our natural environment for future generations. "
        "Small actions can make a big difference when we work together.",
        styles['Normal']
    )
    story.append(content2)
    story.append(Spacer(1, 0.3*inch))
    
    # Section 3
    heading3 = Paragraph("Education and Learning", styles['Heading1'])
    story.append(heading3)
    
    content3 = Paragraph(
        "Education is the foundation of personal and societal growth. "
        "Continuous learning and skill development are essential in today's rapidly changing world. "
        "Online learning platforms and digital resources have made education more accessible than ever before.",
        styles['Normal']
    )
    story.append(content3)
    story.append(Spacer(1, 0.3*inch))
    
    # List section
    list_heading = Paragraph("Key Benefits of Translation Technology:", styles['Heading2'])
    story.append(list_heading)
    
    benefits = [
        "Breaking down language barriers",
        "Facilitating global communication",
        "Preserving document formatting",
        "Enabling accessibility for diverse audiences",
        "Supporting international business"
    ]
    
    for benefit in benefits:
        bullet_point = Paragraph(f"• {benefit}", styles['Normal'])
        story.append(bullet_point)
    
    story.append(Spacer(1, 0.3*inch))
    
    # Conclusion
    conclusion = Paragraph(
        "This document demonstrates various text elements that can be translated while maintaining "
        "the original structure and layout. The translation process preserves the document's "
        "organization and readability across different languages.",
        styles['Normal']
    )
    story.append(conclusion)
    
    # Build PDF
    doc.build(story)
    print(f"Test PDF created: {filename}")

if __name__ == "__main__":
    create_test_pdf()