from agents.scheduler import SchedulerAgent
import time
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('marriage_quotes.log')
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the application."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Marriage Quotes AI - Generate and share marriage quotes')
    parser.add_argument('--run-now', action='store_true', help='Run the job immediately and exit')
    parser.add_argument('--schedule', action='store_true', help='Start the scheduler (default)')
    args = parser.parse_args()

    # Create the scheduler agent
    scheduler_agent = SchedulerAgent()

    # Run based on arguments
    if args.run_now:
        logger.info("Running job immediately")
        scheduler_agent.run_now()
        logger.info("Job completed. Exiting.")
    else:
        # Start the scheduler
        scheduler_agent.start()
        logger.info("Scheduler started. Press Ctrl+C to exit.")
        try:
            # Keep the main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Scheduler stopped.")

if __name__ == "__main__":
    main()
