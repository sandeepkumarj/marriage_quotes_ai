# Marriage Quotes AI

An agentic AI system that generates marriage quotes, creates beautiful images with those quotes, and posts them to Instagram automatically.

## Features

- **Quote Generation**: Uses AI to generate meaningful marriage quotes
- **Image Creation**: Creates visually appealing images with the quotes
- **Instagram Posting**: Automatically posts the images to Instagram
- **Email Dispatch**: Sends the quotes via email
- **Scheduled Execution**: Runs on a schedule (default: every Monday at 9 AM)

## Project Structure

```
marriage_quotes_ai/
├── agents/
│   ├── email_dispatcher.py    # Handles email sending
│   ├── image_creator.py       # Creates images with quotes
│   ├── instagram_poster.py    # Posts images to Instagram
│   ├── quote_generator.py     # Generates marriage quotes
│   └── scheduler.py           # Schedules the agents
├── assets/                    # Directory for assets (created automatically)
├── .env                       # Environment variables (create from .env.example)
├── .env.example               # Example environment variables
├── main.py                    # Main entry point
├── requirements.txt           # Python dependencies
├── test_instagram.py          # Test script for Instagram posting
└── README.md                  # This file
```

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file from `.env.example` and fill in your credentials:
   ```
   cp .env.example .env
   ```
4. Edit the `.env` file with your email and Instagram credentials

### Gmail Configuration

To use Gmail for sending emails:

1. Set up your `.env` file with Gmail credentials:
   ```
   EMAIL_ADDRESS=your_gmail@gmail.com
   EMAIL_PASSWORD=your_app_password
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   RECIPIENT_EMAIL=recipient@example.com
   ```

2. For the `EMAIL_PASSWORD`, you should use an App Password:
   - Go to your Google Account > Security > 2-Step Verification
   - At the bottom, click on "App passwords"
   - Select "Mail" and "Other (Custom name)"
   - Enter a name like "Marriage Quotes App"
   - Copy the generated 16-character password to your `.env` file

3. If you're still having issues, check:
   - https://accounts.google.com/DisplayUnlockCaptcha

## Usage

### Running the Application

You can run the application in two ways:

1. **Scheduler Mode** - Runs on a schedule (default: daily at 9 AM):
   ```
   python main.py
   ```

2. **Immediate Mode** - Runs once immediately and then exits:
   ```
   python main.py --run-now
   ```

### Command Line Options

```
python main.py --help
```

Available options:
- `--run-now`: Run the job immediately and exit
- `--schedule`: Start the scheduler (default behavior)

### Testing Instagram Posting

To test only the Instagram posting functionality:

```
python test_instagram.py
```

## Dependencies

- transformers: For AI quote generation
- Pillow: For image creation
- python-dotenv: For environment variable management
- APScheduler: For scheduling tasks
- instagrapi: For Instagram API integration

## Customization

- Edit `agents/quote_generator.py` to change the quote generation method
- Edit `agents/image_creator.py` to customize the image style
- Edit `agents/scheduler.py` to change the schedule

## License

MIT
