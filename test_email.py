"""
Test script for the email functionality.
This script generates a quote, creates an image, and sends it via email.
"""

import os
from datetime import datetime
from agents.quote_generator import QuoteGenerator
from agents.image_creator import ImageCreator
from agents.email_dispatcher import EmailDispatcher

def test_email():
    """Test the email functionality."""
    print("Starting email test...")
    
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate a quote
    quote_generator = QuoteGenerator()
    quote = quote_generator.generate_quote()
    print(f"Generated quote: {quote}")
    
    # Create an image with the quote
    image_creator = ImageCreator()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(output_dir, f"test_quote_{timestamp}.png")
    image_creator.create_image(quote, filename)
    print(f"Created image: {filename}")
    
    # Send the email
    email_dispatcher = EmailDispatcher()
    recipient = os.getenv('RECIPIENT_EMAIL', 'paofsandeep@gmail.com')
    success = email_dispatcher.send_email(
        subject="Test Marriage Quote",
        body=f"Here's your test marriage quote:\n\n\"{quote}\"\n\nPlease find the attached image.",
        to=recipient,
        attachment_path=filename
    )
    
    if success:
        print(f"Successfully sent email to {recipient}!")
    else:
        print("Failed to send email.")
    
    return success

if __name__ == "__main__":
    test_email()
