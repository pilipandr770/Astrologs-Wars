"""
Script to verify and ensure we have 8 active horoscope blocks
"""
from app import create_app, db
from app.models import BlogBlock
from datetime import datetime

def check_horoscope_blocks():
    """Check if all 8 horoscope blocks exist and are active"""
    app = create_app()
    
    with app.app_context():
        print("Checking horoscope blocks...")
          # Check each position from 1 to 8
        for position in range(1, 9):
            block = BlogBlock.query.filter_by(order=position).first()
            
            if not block:
                print(f"Creating missing block for position {position}")                block = BlogBlock(
                    title=f"Астрологічна система #{position}",
                    content=f"Текст для астрологічної системи #{position}",
                    summary=f"Короткий опис для астрологічної системи #{position}",
                    order=position,
                    is_active=True,
                    created_at=datetime.utcnow()
                )
                db.session.add(block)
            elif not block.is_active:
                print(f"Activating block at position {position}")
                block.is_active = True
            
        # Commit changes
        db.session.commit()
        
        # Count active blocks in positions 1-8
        active_count = BlogBlock.query.filter(
            BlogBlock.is_active == True,
            BlogBlock.position.between(1, 8)
        ).count()
        
        print(f"Active horoscope blocks (positions 1-8): {active_count}")
          # Check shop block (position 12)
        shop_block = BlogBlock.query.filter_by(order=12).first()
        if shop_block:
            print(f"Shop block exists, active: {shop_block.is_active}")
        else:
            print("Shop block does not exist")

if __name__ == "__main__":
    check_horoscope_blocks()
