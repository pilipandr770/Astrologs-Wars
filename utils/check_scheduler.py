"""
Check the scheduler settings in the database
"""
from app import create_app
from app.blog_automation.models import AutopostingSchedule

app = create_app()

with app.app_context():
    schedules = AutopostingSchedule.query.all()
    
    print(f"Found {len(schedules)} autoposting schedules:")
    
    for schedule in schedules:
        print(f"Schedule ID: {schedule.id}")
        print(f"Is active: {schedule.is_active}")
        print(f"Days of week: {schedule.days_of_week}")
        print(f"Posting time: {schedule.posting_time}")
        print(f"Auto translate: {schedule.auto_translate}")
        print(f"Target languages: {schedule.target_languages}")
        print(f"Generate images: {schedule.generate_images}")
        print(f"Post to Telegram: {schedule.post_to_telegram}")
        print("-" * 50)
