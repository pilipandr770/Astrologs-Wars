#!/usr/bin/env python3
"""
Simple script to create BlogBlock entries for horoscope systems.
This script uses the existing database schema with 'position' column.
"""
import os
from app import create_app, db
from app.models import BlogBlock
from datetime import datetime

def create_horoscope_blog_blocks():
    """Create BlogBlock entries for all horoscope systems"""
    # Clean up DATABASE_URL (remove any newlines)
    if 'DATABASE_URL' in os.environ:
        os.environ['DATABASE_URL'] = os.environ['DATABASE_URL'].strip()

    app = create_app()
    
    with app.app_context():
        print("🔧 Creating BlogBlock entries for horoscope systems...")
        
        # Systems for horoscopes (positions 1-8)
        systems = [
            ('Європейська астрологія', 1),
            ('Китайська астрологія', 2),
            ('Індійська астрологія', 3),
            ('Лал Кітаб', 4),
            ('Джйотіш', 5),
            ('Нумерологія', 6),
            ('Таро', 7),
            ('Планетарна астрологія', 8),
        ]
        
        created_count = 0
        
        for name, position in systems:
            # Check if block already exists
            existing_block = BlogBlock.query.filter_by(position=position).first()
            
            if not existing_block:
                # Create new block
                block = BlogBlock(
                    title=name,
                    content=f"Ежедневные гороскопы по системе {name}. Этот блок автоматически обновляется каждый день с новыми прогнозами.",
                    summary=f"Гороскоп на сегодня - {name}",
                    position=position,
                    is_active=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(block)
                print(f"✅ Created: {name} (position={position})")
                created_count += 1
            else:
                # Ensure existing block is active
                existing_block.is_active = True
                existing_block.updated_at = datetime.utcnow()
                print(f"✅ Updated: {name} (position={position}) - set to active")
        
        # Commit changes
        try:
            db.session.commit()
            print(f"\n🎉 BlogBlock creation completed!")
            print(f"📊 Created/Updated: {created_count} blocks")
            
            # List all blocks for verification
            print(f"\n📋 All BlogBlock entries:")
            all_blocks = BlogBlock.query.order_by(BlogBlock.position).all()
            for block in all_blocks:
                print(f"   - Position {block.position}: {block.title} (active: {block.is_active})")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {str(e)}")
            return False

if __name__ == "__main__":
    create_horoscope_blog_blocks()
