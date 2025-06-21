# Horoscope Generator User Guide

This guide explains how to run the horoscope generator script in different environments.

## Development Environment

### Prerequisites
1. Python 3.7+ installed
2. Required Python packages installed from `requirements.txt`
3. `.env` file with proper configuration
4. PostgreSQL database configured

### Running the Generator

To run the horoscope generator once:

```powershell
# Navigate to the project directory
cd path\to\astrolog_wars\work-site

# Run the generator script
python daily_horoscope_sql_fix.py
```

### Setting Up Scheduled Execution

For Windows, you can use the provided batch file:

```powershell
# Run the scheduler
.\run_horoscope_scheduler.bat
```

For PowerShell:

```powershell
# Run the scheduler
.\run_horoscope_scheduler.ps1
```

## Production Environment (Render)

### One-time Setup

1. Make sure your `render.yaml` is configured properly:

```yaml
services:
  # Existing web service configuration...
  
  # Horoscope generator scheduled job
  - type: cron
    name: daily-horoscope-generator
    runtime: python
    plan: starter
    schedule: "0 4 * * *"  # Run every day at 4:00 AM UTC
    buildCommand: pip install -r requirements.txt
    startCommand: python daily_horoscope_sql_fix.py
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: astro_blog_db
          property: connectionString
      # Include all other required environment variables
```

2. Deploy to Render using the Render Dashboard or CLI

### Manual Execution on Render

If you need to run the generator manually on Render:

1. Navigate to your Render Dashboard
2. Find the `daily-horoscope-generator` service
3. Click "Manual Deploy" and choose "Clear Build Cache & Deploy"

## Environment Variables

Ensure the following environment variables are set:

```
DATABASE_URL=postgresql://username:password@host:port/astro_blog_db
OPENAI_API_KEY=your_openai_api_key
FLASK_APP=app
FLASK_ENV=production
EUROPEAN_ASTROLOGY_ASSISTANT_ID=asst_xxxx
CHINESE_ASTROLOGY_ASSISTANT_ID=asst_xxxx
INDIAN_ASTROLOGY_ASSISTANT_ID=asst_xxxx
LAL_KITAB_ASSISTANT_ID=asst_xxxx
JYOTISH_ASSISTANT_ID=asst_xxxx
NUMEROLOGY_ASSISTANT_ID=asst_xxxx
TAROT_ASSISTANT_ID=asst_xxxx
PLANETARY_ASTROLOGY_ASSISTANT_ID=asst_xxxx
UKRAINIAN_TRANSLATION_ASSISTANT_ID=asst_xxxx  # Add this for Ukrainian translations
TELEGRAM_BOT_TOKEN=your_telegram_bot_token     # Optional for notifications
TELEGRAM_CHAT_ID=your_telegram_chat_id         # Optional for notifications
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Verify that the `DATABASE_URL` is correct with no whitespace
   - Check that the database exists and is accessible
   - Make sure the port number is included (default: 5432)

2. **OpenAI API Errors**:
   - Verify your `OPENAI_API_KEY` is valid
   - Check that all assistant IDs are correct
   - Note that the Assistants API is deprecated, future versions may use the Responses API

3. **Missing Ukrainian Translations**:
   - Add a `UKRAINIAN_TRANSLATION_ASSISTANT_ID` environment variable
   - Alternatively, modify the script to handle missing translation IDs gracefully

4. **Blank or Duplicate Horoscopes**:
   - Run `clean_html_blocks.py` to clean existing database content
   - Verify that your OpenAI API calls are working correctly

For more detailed troubleshooting, check the `horoscope_generator.log` file which contains detailed logs of the script execution.

## Maintenance

Regularly check the following:

1. OpenAI API version changes (particularly the transition from Assistants API to Responses API)
2. Database schema changes that might require updates to the generator script
3. Log files for errors or warnings
4. Generated content quality and completeness
