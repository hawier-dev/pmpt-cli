#!/usr/bin/env python3
"""
Create a simple icon for PMPT CLI
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a simple PMPT CLI icon"""
    # Create a 256x256 image with transparent background
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a rounded rectangle background
    margin = 20
    radius = 30
    
    # Background gradient effect
    for i in range(margin, size - margin):
        alpha = int(255 * (i - margin) / (size - 2 * margin))
        color = (64, 156, 255, min(alpha, 255))  # Blue gradient
        draw.rectangle([margin, i, size - margin, i + 1], fill=color)
    
    # Draw rounded corners (simple approach)
    corner_size = radius
    draw.rectangle([margin, margin, margin + corner_size, margin + corner_size], fill=(64, 156, 255, 255))
    draw.rectangle([size - margin - corner_size, margin, size - margin, margin + corner_size], fill=(64, 156, 255, 255))
    draw.rectangle([margin, size - margin - corner_size, margin + corner_size, size - margin], fill=(64, 156, 255, 255))
    draw.rectangle([size - margin - corner_size, size - margin - corner_size, size - margin, size - margin], fill=(64, 156, 255, 255))
    
    # Try to load a font, fallback to default
    try:
        font_size = 48
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Draw text
    text = "PMPT"
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center text
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 10
    
    # Draw text with shadow
    draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, 128))  # Shadow
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))  # Main text
    
    # Draw subtitle
    try:
        subtitle_font = ImageFont.truetype("arial.ttf", 16)
    except:
        subtitle_font = ImageFont.load_default()
    
    subtitle = "CLI"
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    
    subtitle_x = (size - subtitle_width) // 2
    subtitle_y = y + text_height + 5
    
    draw.text((subtitle_x + 1, subtitle_y + 1), subtitle, font=subtitle_font, fill=(0, 0, 0, 128))
    draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill=(200, 200, 200, 255))
    
    # Save as ICO
    img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print("✅ Created icon.ico")

if __name__ == "__main__":
    try:
        create_icon()
    except ImportError:
        print("⚠️  PIL not available, creating placeholder icon")
        # Create a simple placeholder
        with open('icon.ico', 'wb') as f:
            # Minimal ICO header (not a real icon, but prevents build errors)
            f.write(b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00\x16\x00\x00\x00' + b'\x00' * 1384)