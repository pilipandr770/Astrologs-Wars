"""
Script to verify Ukrainian language support in the system
"""
from app import create_app
from app.models import BlogBlock
from app.blog_automation.models import AutopostingSchedule
import sys
from flask import g

app = create_app()

def check_languages_config():
    """Check languages configuration in the app"""
    print("=== Languages Configuration ===")
    print(f"Supported languages: {app.config.get('LANGUAGES')}")
    return 'uk' in app.config.get('LANGUAGES', [])

def check_autoposting_schedule():
    """Check if Ukrainian is in target languages for autoposting schedule"""
    with app.app_context():
        schedules = AutopostingSchedule.query.filter_by(is_active=True).all()
        print("\n=== Autoposting Schedules ===")
        for schedule in schedules:
            print(f"Schedule ID: {schedule.id}")
            print(f"Target languages: {schedule.target_languages}")
            languages = schedule.target_languages.split(',')
            if 'uk' in languages:
                print("✓ Ukrainian language is included in target languages")
                return True
            else:
                print("✗ Ukrainian language is NOT included in target languages")
                return False

def check_blog_translations(lang='uk'):
    """Check if blog blocks have Ukrainian translations"""
    with app.app_context():
        blocks = BlogBlock.query.filter_by(is_active=True).all()
        print(f"\n=== Blog Translations for '{lang}' ===")
        blocks_with_translation = 0
        
        field_prefix = 'ua' if lang == 'uk' else lang
        
        for block in blocks:
            title_field = f'title_{field_prefix}'
            content_field = f'content_{field_prefix}'
            summary_field = f'summary_{field_prefix}'
            
            has_title = hasattr(block, title_field) and getattr(block, title_field)
            has_content = hasattr(block, content_field) and getattr(block, content_field)
            has_summary = hasattr(block, summary_field) and getattr(block, summary_field)
            
            if has_title or has_content or has_summary:
                blocks_with_translation += 1
                status = "✓"
            else:
                status = "✗"
                
            print(f"{status} Block {block.position} ({block.title}): Title: {has_title}, Content: {has_content}, Summary: {has_summary}")
        
        print(f"\n{blocks_with_translation} out of {len(blocks)} blocks have '{lang}' translations")
        return blocks_with_translation > 0

def check_astro_systems():
    """Check if astrology systems have Ukrainian names"""
    try:
        sys.path.append('c:\\Users\\ПК\\astrolog_wars\\work-site')
        from daily_horoscope_generator import ASTRO_SYSTEMS
        
        print("\n=== Astrology Systems Language Support ===")
        systems_with_uk = 0
        
        for system in ASTRO_SYSTEMS:
            has_uk = 'name_uk' in system
            status = "✓" if has_uk else "✗"
            print(f"{status} {system['name']}: {'name_uk' in system}")
            if has_uk:
                systems_with_uk += 1
        
        print(f"\n{systems_with_uk} out of {len(ASTRO_SYSTEMS)} astrology systems have Ukrainian names")
        return systems_with_uk == len(ASTRO_SYSTEMS)
    except ImportError:
        print("Could not import ASTRO_SYSTEMS from daily_horoscope_generator.py")
        return False

if __name__ == "__main__":
    success_count = 0
    
    if check_languages_config():
        success_count += 1
        
    if check_autoposting_schedule():
        success_count += 1
        
    if check_blog_translations('uk'):
        success_count += 1
    
    if check_astro_systems():
        success_count += 1
    
    print("\n=== Summary ===")
    print(f"{success_count}/4 Ukrainian language integration checks passed")
    
    if success_count == 4:
        print("✓ Ukrainian language is fully integrated in the system!")
    else:
        print("! Some aspects of Ukrainian language integration need attention.")
