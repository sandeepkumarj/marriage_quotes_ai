import os
import time
import logging
from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ClientError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

class InstagramPoster:
    """
    Agent responsible for posting images to Instagram.
    Uses instagrapi library for Instagram API interactions.
    """
    
    def __init__(self):
        """Initialize the Instagram client and attempt to log in."""
        self.client = Client()
        self.username = os.getenv('INSTAGRAM_USERNAME')
        self.password = os.getenv('INSTAGRAM_PASSWORD')
        
        # Check if session exists
        session_file = "instagram_session.json"
        if os.path.exists(session_file):
            try:
                self.client.load_settings(session_file)
                self.client.get_timeline_feed()  # Test if session is valid
                logger.info("Successfully loaded existing Instagram session")
            except LoginRequired:
                logger.info("Session expired, logging in again")
                self._login()
        else:
            self._login()
    
    def _login(self):
        """Log in to Instagram and save the session."""
        try:
            self.client.login(self.username, self.password)
            self.client.dump_settings("instagram_session.json")
            logger.info(f"Successfully logged in as {self.username}")
        except Exception as e:
            logger.error(f"Failed to log in to Instagram: {str(e)}")
            raise
    
    def post_image(self, image_path, caption):
        """
        Post an image to Instagram with the given caption.
        
        Args:
            image_path (str): Path to the image file
            caption (str): Caption for the Instagram post
        
        Returns:
            bool: True if posting was successful, False otherwise
        """
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return False
        
        try:
            # Add hashtags to the caption
            full_caption = f"{caption}\n\n#marriage #marriagequotes #love #relationship #godlymarriage"
            
            # Upload the image
            media = self.client.photo_upload(
                image_path,
                full_caption
            )
            
            logger.info(f"Successfully posted image to Instagram. Media ID: {media.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to post image to Instagram: {str(e)}")
            # Try to re-login and post again
            try:
                self._login()
                media = self.client.photo_upload(image_path, full_caption)
                logger.info(f"Successfully posted image after re-login. Media ID: {media.id}")
                return True
            except Exception as e2:
                logger.error(f"Failed to post image after re-login: {str(e2)}")
                return False
