from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import logging
import os
from dotenv import load_dotenv
from agents.quote_generator import QuoteGenerator
from agents.image_creator import ImageCreator
from agents.email_dispatcher import EmailDispatcher
from agents.instagram_poster import InstagramPoster

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class SchedulerAgent:
    """
    Agent responsible for scheduling and coordinating the other agents.
    Handles the workflow of generating quotes, creating images,
    sending emails, and posting to Instagram.
    """

    def __init__(self):
        """Initialize the scheduler and all other agents."""
        self.scheduler = BackgroundScheduler()
        self.quote_generator = QuoteGenerator()
        self.image_creator = ImageCreator()
        self.email_dispatcher = EmailDispatcher()
        self.instagram_poster = InstagramPoster()

        # Create output directory if it doesn't exist
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)

        # Get recipient email from environment or use default
        self.recipient_email = os.getenv('RECIPIENT_EMAIL', 'paofsandeep@gmail.com')

    def job(self):
        """
        Main job that runs on schedule.
        Generates a quote, creates an image, sends an email, and posts to Instagram.
        """
        try:
            logger.info("Starting scheduled job")

            # Generate quote
            quote = self.quote_generator.generate_quote()
            logger.info(f"Generated quote: {quote}")

            # Create image with the quote
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(self.output_dir, f"quote_{timestamp}.png")
            self.image_creator.create_image(quote, filename)
            logger.info(f"Created image: {filename}")

            # Send email with the quote image
            email_sent = self.email_dispatcher.send_email(
                subject="Your Daily Marriage Quote",
                body=f"Here's your marriage quote for today:\n\n\"{quote}\"\n\nPlease find the attached image.",
                to=self.recipient_email,
                attachment_path=filename
            )

            if email_sent:
                logger.info(f"Email sent to {self.recipient_email}")
            else:
                logger.warning("Failed to send email")

            # Post to Instagram
            instagram_posted = self.instagram_poster.post_image(
                image_path=filename,
                caption=f"Today's Marriage Quote: {quote}"
            )

            if instagram_posted:
                logger.info("Posted to Instagram successfully")
            else:
                logger.warning("Failed to post to Instagram")

            logger.info("Scheduled job completed")

        except Exception as e:
            logger.error(f"Error in scheduled job: {str(e)}")

    def start(self):
        """Start the scheduler with the configured job."""
        # Schedule the job to run every day at 9 AM
        self.scheduler.add_job(self.job, 'cron', hour=9, minute=0)
        logger.info("Scheduler started. Job will run daily at 9:00 AM")
        self.scheduler.start()

    def run_now(self):
        """Run the job immediately, without waiting for the schedule."""
        logger.info("Running job immediately")
        self.job()
