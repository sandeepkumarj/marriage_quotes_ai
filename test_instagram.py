"""
Test script for the Instagram posting functionality.
This script generates a quote, creates an image, and posts it to Instagram.
"""

import os
from agents.quote_generator import QuoteGenerator
from agents.image_creator import ImageCreator
from agents.instagram_poster import InstagramPoster
from datetime import datetime

def test_instagram_posting():
    """Test the Instagram posting functionality."""
    print("Starting Instagram posting test...")
    
    # Generate a quote
    quote_generator = QuoteGenerator()
    quote = quote_generator.generate_quote()
    print(f"Generated quote: {quote}")
    
    # Create an image with the quote
    image_creator = ImageCreator()
    filename = f"test_quote_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    image_creator.create_image(quote, filename)
    print(f"Created image: {filename}")
    
    # Post the image to Instagram
    instagram_poster = InstagramPoster()
    success = instagram_poster.post_image(
        image_path=filename,
        caption=f"Test Marriage Quote: {quote}"
    )
    
    if success:
        print("Successfully posted image to Instagram!")
    else:
        print("Failed to post image to Instagram.")
    
    return success

if __name__ == "__main__":
    test_instagram_posting()
