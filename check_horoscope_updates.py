"""
Script to check if horoscopes are being updated correctly in the database
"""
from app import create_app, db
from app.models import BlogBlock
from datetime import datetime, timedelta

def check_horoscope_updates():
    """Check when horoscope blocks were last updated"""
    app = create_app()
    
    with app.app_context():
        print("Checking horoscope block update timestamps...")
        
        # Get all horoscope blocks (positions 1-8)
        blocks = BlogBlock.query.filter(
            BlogBlock.position.between(1, 8)
        ).order_by(BlogBlock.position).all()
        
        today = datetime.utcnow().date()
        today_str = today.strftime("%Y-%m-%d")
        
        print(f"Current date: {today_str}")
        print("-" * 60)
        print("Position | System | Last Updated | Status")
        print("-" * 60)
        
        for block in blocks:
            # Get the last update timestamp as date only
            last_updated = block.updated_at.date() if block.updated_at else None
            last_updated_str = last_updated.strftime("%Y-%m-%d") if last_updated else "Never"
            
            # Check if the block was updated today
            is_current = (last_updated == today) if last_updated else False
            status = "Current" if is_current else "Outdated"
            
            # If updated today, check if the content mentions today's date
            if is_current:
                # Extract the first title paragraph as system name
                system_name = block.title.split('\n')[0] if block.title else f"System #{block.position}"
                
                # Check if content contains today's date in any format
                today_formats = [
                    today.strftime("%Y-%m-%d"), 
                    today.strftime("%d.%m.%Y"),
                    today.strftime("%B %d, %Y"),
                    today.strftime("%d %B %Y")
                ]
                
                content_has_today = False
                for date_format in today_formats:
                    if block.content and date_format in block.content:
                        content_has_today = True
                        break
                
                if content_has_today:
                    status += " (Today's date in content)"
            else:
                system_name = f"System #{block.position}"
            
            print(f"{block.position:8} | {system_name[:10]:10} | {last_updated_str:12} | {status}")
        
        print("-" * 60)
        
        # Also check if there are any draft or inactive horoscope blocks
        inactive = BlogBlock.query.filter(
            BlogBlock.is_active == False,
            BlogBlock.position.between(1, 8)
        ).count()
        
        if inactive > 0:
            print(f"Warning: There are {inactive} inactive horoscope blocks")
        else:
            print("All horoscope blocks are active")

if __name__ == "__main__":
    check_horoscope_updates()
