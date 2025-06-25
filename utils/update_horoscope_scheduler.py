"""
Script to update the horoscope scheduler to use the integrated image generator
"""
import os
import sys
from datetime import datetime

def update_scheduler():
    """Updates scheduler files for horoscope generation with images"""
    print("Updating horoscope scheduler files...")
    
    # Update the scheduler.py file if it exists
    scheduler_path = os.path.join(os.getcwd(), 'schedule_horoscopes.py')
    if os.path.exists(scheduler_path):
        with open(scheduler_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if already updated
        if 'daily_horoscope_with_images.py' in content:
            print("Scheduler already updated to use integrated image generator.")
        else:
            # Replace with new script
            content = content.replace('daily_horoscope_generator.py', 'daily_horoscope_with_images.py')
            content = content.replace('daily_horoscope_sql_fix.py', 'daily_horoscope_with_images.py')
            
            # Add comment about update
            current_date = datetime.now().strftime('%Y-%m-%d')
            comment = f"# Updated on {current_date} to use integrated horoscope generator with images\n"
            lines = content.split('\n')
            if lines and lines[0].startswith('#!'):
                lines.insert(1, comment)
            else:
                lines.insert(0, comment)
                
            content = '\n'.join(lines)
            
            # Write back
            with open(scheduler_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"Updated {scheduler_path} to use integrated horoscope generator.")
    else:
        print(f"Scheduler file not found at {scheduler_path}")
        
    # Update batch files if they exist
    scheduler_bat = os.path.join(os.getcwd(), 'run_horoscope_scheduler.bat')
    if os.path.exists(scheduler_bat):
        with open(scheduler_bat, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'daily_horoscope_with_images.py' in content:
            print("Batch file already updated.")
        else:
            content = content.replace('daily_horoscope_generator.py', 'daily_horoscope_with_images.py')
            content = content.replace('daily_horoscope_sql_fix.py', 'daily_horoscope_with_images.py')
            
            with open(scheduler_bat, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"Updated {scheduler_bat}")
    
    print("Update complete.")

if __name__ == "__main__":
    update_scheduler()
