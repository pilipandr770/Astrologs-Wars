# Astrology Site Project Structure

## Core Components

### Active Files (Used in Production)

1. **Main Web Application Files:**
   - `wsgi.py` - Entry point for Gunicorn WSGI server
   - `requirements.txt` - Project dependencies
   - `render.yaml` - Configuration for deployment on Render platform
   - `build_render.sh`, `prestart.sh` - Scripts for building and launching on Render

2. **Active Horoscope Generation Scripts:**
   - `daily_horoscope_replace.py` - **CURRENT ACTIVE** script for horoscope generation with replacement of old ones and image generation via DALL-E 3 (updated June 25, 2025)
   - `translator.py` - Module for automatic translation of horoscopes into English, German, and Russian
   - `test_translator.py` - Script for testing translation functionality
   - `force_cleanup_horoscope_images.py` - Script for cleaning up old horoscope images
   - `check_horoscope_images.py` - Horoscope image verification
   - `daily_horoscope_with_images.py` - Alternative script with image generation
   - `schedule_horoscopes.py` - Horoscope generation scheduler

3. **Database Management Scripts:**
   - `create_tables.py` - Database initialization
   - `init_db.py` - Database initial setup
   - `recreate_admin.py` - Admin user recreation

4. **Launch Scripts:**
   - `run_horoscope_replace.bat/.sh/.ps1` - Standard horoscope generation
   - `run_horoscope_with_translations.bat/.sh/.ps1` - Horoscope generation with translations
   - `run_horoscope_with_dalle.bat/.sh/.ps1` - Horoscope generation with DALL-E images
   - `run_horoscope_full.bat/.sh/.ps1` - Full horoscope generation (translations + DALL-E)
   - `test_translator.bat/.sh/.ps1` - Translation functionality test

### Directory Structure

1. **Main Directories:**
   - `/app` - Main application code
   - `/app/static` - Static files (CSS, JavaScript, images)
   - `/app/templates` - HTML templates
   - `/app/models` - Database models
   - `/app/blog_automation` - Blog automation system
   - `/utils` - Utility scripts
   - `/docs` - Documentation

2. **Archive Directories:**
   - `/archive` - Obsolete scripts and files
   - `/archive/horoscope_generators` - Old horoscope generation scripts
   - `/archive/fixes` - Fix scripts that are no longer relevant
   - `/archive/docs` - Outdated documentation
   - `/archive/tests` - Test and verification scripts

## Workflow and Maintenance

### Horoscope Generation

The current workflow uses `daily_horoscope_replace.py`, which:

1. Generates new horoscope texts in Ukrainian
2. Translates texts into English, German, and Russian (if enabled)
3. Creates images for each system (locally or via DALL-E 3)
4. Replaces existing records instead of creating new ones
5. Cleans up old unused images

Manual execution:

**Standard execution** (Windows/Linux/Mac):
```
run_horoscope_replace.bat / .sh / .ps1
```

**With translations enabled** (Windows/Linux/Mac):
```
run_horoscope_with_translations.bat / .sh / .ps1
```

**With DALL-E images** (Windows/Linux/Mac):
```
run_horoscope_with_dalle.bat / .sh / .ps1
```

**Full execution with translations and DALL-E** (Windows/Linux/Mac):
```
run_horoscope_full.bat / .sh / .ps1
```

### Translation Testing

To test the translator functionality:
```
test_translator.bat / .sh / .ps1
```

### Database Operations

Database operations are performed via:
- Flask-SQLAlchemy ORM
- SQLAlchemy Core for raw SQL when needed
- Database migration scripts in `/migrations` folder

### Deployment

The Render configuration in `render.yaml` includes:
- Web service for the main application
- Cron job for daily horoscope generation
- Redis for caching

## Code Maintenance Principles

1. **Follow Directory Structure:**
   - New scripts should be placed in appropriate directories
   - Do not create new files in the project root without necessity

2. **Versioning and Archiving:**
   - Before significant changes, copy working scripts with new names
   - Move obsolete scripts to `/archive`

3. **Documentation:**
   - Update documentation when making changes
   - Use code comments for complex sections

4. **Testing:**
   - Test changes locally before deployment
   - Use `check_*.py` scripts for verification

## Documentation

Main project documentation:

1. **General Documentation:**
   - `PROJECT_STRUCTURE.md` - Project structure (Ukrainian)
   - `PROJECT_STRUCTURE_EN.md` - Project structure (English)
   - `README.md` - General project information
   - `FINAL_SUCCESS_REPORT.md` - Report on successful project reorganization

2. **Horoscope Generation:**
   - `/docs/HOROSCOPE_TRANSLATION_GUIDE.md` - Horoscope translation guide (Ukrainian)
   - `/docs/HOROSCOPE_TRANSLATION_GUIDE_EN.md` - Horoscope translation guide (English)
   - `/docs/MULTILINGUAL_HOROSCOPE_QUICKREF.md` - Quick reference for multilingual horoscopes
   - `/docs/DALLE_HOROSCOPE_INTEGRATION.md` - DALL-E integration for image generation
   - `translator_README.md` - Technical documentation for the translator module

## Environment Variables

Main project environment variables (.env):

1. **Basic Settings:**
   - `DATABASE_URL` - Database connection URL
   - `SECRET_KEY` - Flask secret key
   - `DEBUG` - Debug mode (true/false)

2. **OpenAI and DALL-E Integration:**
   - `OPENAI_API_KEY` - API key for OpenAI
   - `USE_DALLE_IMAGES` - Use DALL-E for images (true/false)
   - `DALLE_IMAGE_SIZE` - DALL-E image size (1024x1024, 1792x1024, 1024x1792)
   - `DALLE_IMAGE_QUALITY` - DALL-E image quality (standard, hd)

3. **Translator Settings:**
   - `USE_TRANSLATIONS` - Enable automatic translation (true/false)
   - `OPENAI_TRANSLATION_ASSISTANT_ID` - ID of the translation assistant
   - `TRANSLATION_MAX_RETRIES` - Maximum number of translation attempts
   - `TRANSLATION_TIMEOUT_SECONDS` - Translation timeout

## Commonly Used Commands

1. **Starting the Local Server:**
   ```
   flask run
   ```

2. **Database Management:**
   ```
   flask db migrate -m "Migration description"
   flask db upgrade
   ```

3. **Horoscope Generation:**
   ```
   python daily_horoscope_replace.py
   ```

4. **File Operations:**
   ```
   python manage_images.py cleanup
   ```

5. **Deployment:**
   ```
   ./build_render.sh
   ```

## Additional Resources

- Render Dashboard: [https://dashboard.render.com/](https://dashboard.render.com/)
- Project Repository: [https://github.com/yourusername/astrology-site](https://github.com/yourusername/astrology-site)
- OpenAI Documentation: [https://platform.openai.com/docs/](https://platform.openai.com/docs/)
