"""
Update target languages to include Ukrainian
"""
from app import create_app
from app.blog_automation.models import AutopostingSchedule
from app.models import db

app = create_app()

with app.app_context():
    # Find the active schedule
    schedule = AutopostingSchedule.query.filter_by(is_active=True).first()
    
    if schedule:
        print(f"Current target languages: {schedule.target_languages}")
        
        # Update to include Ukrainian
        if 'uk' not in schedule.target_languages.split(','):
            languages = schedule.target_languages.split(',')
            languages.append('uk')
            schedule.target_languages = ','.join(languages)
            db.session.commit()
            print(f"Updated target languages: {schedule.target_languages}")
        else:
            print("Ukrainian language is already included")
    else:
        print("No active schedule found")
