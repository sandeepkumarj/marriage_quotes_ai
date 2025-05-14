from PIL import Image, ImageDraw, ImageFont
import os
import random
import textwrap
from pathlib import Path

class ImageCreator:
    def __init__(self):
        """Initialize the ImageCreator with default settings."""
        # Create assets directory if it doesn't exist
        self.assets_dir = Path("assets")
        self.assets_dir.mkdir(exist_ok=True)

        # Instagram-friendly dimensions (1080x1080 for square posts)
        self.width = 1080
        self.height = 1080

        # Try to load a nice font, fall back to default if not available
        try:
            # Common fonts that might be available
            font_options = [
                "Arial.ttf", "Helvetica.ttf", "Georgia.ttf",
                "Times New Roman.ttf", "Verdana.ttf"
            ]

            # Try to find a font that exists
            for font_name in font_options:
                # Check common font locations
                font_paths = [
                    f"/Library/Fonts/{font_name}",
                    f"/System/Library/Fonts/{font_name}",
                    f"C:\\Windows\\Fonts\\{font_name}",
                    f"/usr/share/fonts/truetype/{font_name}"
                ]

                for path in font_paths:
                    if os.path.exists(path):
                        self.main_font = ImageFont.truetype(path, 48)
                        self.small_font = ImageFont.truetype(path, 24)
                        break

                if hasattr(self, 'main_font'):
                    break

            if not hasattr(self, 'main_font'):
                # Fall back to default font
                self.main_font = ImageFont.load_default()
                self.small_font = ImageFont.load_default()

        except Exception:
            # If any error occurs, use default font
            self.main_font = ImageFont.load_default()
            self.small_font = ImageFont.load_default()

        # Background colors (pastel colors that work well with black text)
        self.bg_colors = [
            (255, 240, 245),  # Lavender Blush
            (240, 255, 240),  # Honeydew
            (255, 250, 240),  # Floral White
            (240, 248, 255),  # Alice Blue
            (255, 245, 238),  # Seashell
            (245, 255, 250),  # Mint Cream
            (240, 255, 255),  # Azure
            (255, 255, 240),  # Ivory
        ]

    def create_image(self, text, filename):
        """
        Create an Instagram-friendly image with the given quote text.

        Args:
            text (str): The quote text to put on the image
            filename (str): The filename to save the image as
        """
        # Create a new image with a random background color
        bg_color = random.choice(self.bg_colors)
        img = Image.new('RGB', (self.width, self.height), color=bg_color)
        draw = ImageDraw.Draw(img)

        # Add a subtle border
        border_width = 20
        draw.rectangle(
            [(border_width, border_width),
             (self.width - border_width, self.height - border_width)],
            outline=(200, 200, 200),
            width=2
        )

        # Wrap text to fit within the image
        margin = 100
        wrapper = textwrap.TextWrapper(width=30)  # Adjust width based on font size
        word_list = wrapper.wrap(text=text)

        # Calculate text height to center it
        text_height = len(word_list) * 60  # Approximate line height
        y_text = (self.height - text_height) // 2

        # Draw each line of wrapped text
        for line in word_list:
            # Get width of this line (using getbbox for newer Pillow versions)
            try:
                # For newer Pillow versions
                bbox = self.main_font.getbbox(line)
                line_width = bbox[2] - bbox[0]
            except AttributeError:
                # Fallback for older Pillow versions
                try:
                    line_width, _ = draw.textsize(line, font=self.main_font)
                except AttributeError:
                    # Last resort fallback
                    line_width = self.width // 2

            # Calculate x position to center the line
            x_text = (self.width - line_width) // 2

            # Draw the text
            draw.text(
                (x_text, y_text),
                line,
                font=self.main_font,
                fill=(0, 0, 0)  # Black text
            )
            y_text += 60  # Move to next line position

        # Add a small watermark/attribution
        watermark = "Marriage Quotes AI"

        # Get watermark dimensions (using getbbox for newer Pillow versions)
        try:
            # For newer Pillow versions
            bbox = self.small_font.getbbox(watermark)
            watermark_width = bbox[2] - bbox[0]
            watermark_height = bbox[3] - bbox[1]
        except AttributeError:
            # Fallback for older Pillow versions
            try:
                watermark_width, watermark_height = draw.textsize(watermark, font=self.small_font)
            except AttributeError:
                # Last resort fallback
                watermark_width, watermark_height = 200, 20
        draw.text(
            (self.width - watermark_width - 40, self.height - watermark_height - 30),
            watermark,
            font=self.small_font,
            fill=(100, 100, 100)  # Gray text
        )

        # Save the image
        img.save(filename, quality=95)  # High quality for Instagram
