#!/usr/bin/env python3
"""
Script to migrate BlogBlock data from position to order column and create missing blog blocks.
This script should be run in the Render environment.
"""
import os
from app import create_app, db
from app.models import BlogBlock
from datetime import datetime

def migrate_and_create_blog_blocks():
    """Migrate existing BlogBlock data and create missing blocks"""
    # Clean up DATABASE_URL (remove any newlines)
    if 'DATABASE_URL' in os.environ:
        os.environ['DATABASE_URL'] = os.environ['DATABASE_URL'].strip()

    app = create_app()
    
    with app.app_context():
        print("🔄 Migrating BlogBlock model and creating missing blocks...")
        
        # First, ensure all tables are created with the new schema
        db.create_all()
        
        # Define the blog blocks we need for the horoscope systems
        horoscope_systems = [
            {'name': 'Європейська астрологія', 'order': 1},
            {'name': 'Китайська астрологія', 'order': 2},
            {'name': 'Індійська астрологія', 'order': 3},
            {'name': 'Лал Кітаб', 'order': 4},
            {'name': 'Джйотіш', 'order': 5},
            {'name': 'Нумерологія', 'order': 6},
            {'name': 'Таро', 'order': 7},
            {'name': 'Планетарна астрологія', 'order': 8},
        ]
        
        created_count = 0
        updated_count = 0
        
        for system in horoscope_systems:
            # Check if block already exists
            existing_block = BlogBlock.query.filter_by(order=system['order']).first()
            
            if existing_block:
                # Update existing block
                existing_block.title = system['name']
                existing_block.is_active = True
                existing_block.updated_at = datetime.utcnow()
                print(f"✅ Updated existing block: {system['name']} (order={system['order']})")
                updated_count += 1
            else:
                # Create new block
                new_block = BlogBlock(
                    title=system['name'],
                    content=f"Ежедневные гороскопы по системе {system['name']}. Этот блок будет автоматически обновляться каждый день.",
                    summary=f"Гороскоп на сегодня - {system['name']}",
                    order=system['order'],
                    is_active=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(new_block)
                print(f"✅ Created new block: {system['name']} (order={system['order']})")
                created_count += 1
        
        # Also create a shop block at position 12 if it doesn't exist
        shop_block = BlogBlock.query.filter_by(order=12).first()
        if not shop_block:
            shop_block = BlogBlock(
                title="Астрологічні товари",
                content="Персоналізовані астрологічні товари та послуги",
                summary="Магазин астрологічних товарів",
                order=12,
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(shop_block)
            print(f"✅ Created shop block at order=12")
            created_count += 1
        
        # Commit all changes
        try:
            db.session.commit()
            print(f"\n🎉 Migration completed successfully!")
            print(f"📊 Created: {created_count} blocks")
            print(f"📊 Updated: {updated_count} blocks")
            
            # Verify all blocks exist
            print(f"\n📋 Verifying all BlogBlock entries:")
            all_blocks = BlogBlock.query.order_by(BlogBlock.order).all()
            for block in all_blocks:
                print(f"   - Order {block.order}: {block.title} (active: {block.is_active})")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during migration: {str(e)}")
            return False

if __name__ == "__main__":
    migrate_and_create_blog_blocks()
