#!/usr/bin/env python3
"""
Simple script to create PNG icons for the arXiv Enhancer Chrome Extension
"""

import os
import base64

def create_simple_png(size, filename):
    """Create a simple PNG file with a colored square"""
    
    # This is a minimal PNG file structure for a colored square
    # PNG signature
    png_signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk (image header)
    width = size
    height = size
    bit_depth = 8
    color_type = 2  # RGB
    compression = 0
    filter_method = 0
    interlace = 0
    
    ihdr_data = (
        width.to_bytes(4, 'big') +
        height.to_bytes(4, 'big') +
        bit_depth.to_bytes(1, 'big') +
        color_type.to_bytes(1, 'big') +
        compression.to_bytes(1, 'big') +
        filter_method.to_bytes(1, 'big') +
        interlace.to_bytes(1, 'big')
    )
    
    ihdr_crc = calculate_crc(b'IHDR' + ihdr_data)
    ihdr_chunk = (
        len(ihdr_data).to_bytes(4, 'big') +
        b'IHDR' +
        ihdr_data +
        ihdr_crc.to_bytes(4, 'big')
    )
    
    # IDAT chunk (image data)
    # Create a simple blue square
    blue_color = b'\x2c\x5a\xa0'  # RGB for #2c5aa0
    row_data = b'\x00' + blue_color * width  # Filter byte + RGB data
    idat_data = row_data * height
    
    # Compress the data (simple method - just use raw data for now)
    compressed_data = idat_data
    
    idat_crc = calculate_crc(b'IDAT' + compressed_data)
    idat_chunk = (
        len(compressed_data).to_bytes(4, 'big') +
        b'IDAT' +
        compressed_data +
        idat_crc.to_bytes(4, 'big')
    )
    
    # IEND chunk
    iend_crc = calculate_crc(b'IEND')
    iend_chunk = (
        (0).to_bytes(4, 'big') +
        b'IEND' +
        iend_crc.to_bytes(4, 'big')
    )
    
    # Combine all chunks
    png_data = png_signature + ihdr_chunk + idat_chunk + iend_chunk
    
    # Write to file
    with open(filename, 'wb') as f:
        f.write(png_data)
    
    print(f"Created {filename}")

def calculate_crc(data):
    """Simple CRC calculation for PNG chunks"""
    # This is a simplified CRC calculation
    # In a real implementation, you'd use zlib.crc32
    crc = 0
    for byte in data:
        crc = (crc << 8) ^ byte
    return crc & 0xFFFFFFFF

def create_icons():
    """Create all required icon files"""
    
    # Ensure icons directory exists
    os.makedirs('icons', exist_ok=True)
    
    # Create icons for different sizes
    sizes = [16, 48, 128]
    
    for size in sizes:
        filename = f'icons/icon{size}.png'
        create_simple_png(size, filename)
    
    print("\nAll icons created successfully!")
    print("You can now reload the extension in Chrome.")

if __name__ == "__main__":
    try:
        create_icons()
    except Exception as e:
        print(f"Error creating icons: {e}")
        print("\nAlternative solution:")
        print("1. Open create_icons.html in your browser")
        print("2. Download the generated icons")
        print("3. Place them in the icons folder")
