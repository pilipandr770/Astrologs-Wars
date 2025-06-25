#!/usr/bin/env python3
"""
Quick test script to verify that the daily horoscope generator can find all blog blocks.
"""
import os
from app import create_app, db
from app.models import BlogBlock

def test_blog_blocks():
    """Test that all blog blocks can be found by order"""
    # Clean up DATABASE_URL (remove any newlines)
    if 'DATABASE_URL' in os.environ:
        os.environ['DATABASE_URL'] = os.environ['DATABASE_URL'].strip()

    app = create_app()
    
    with app.app_context():
        print("🔍 Testing blog block lookups...")
        
        # Test the systems that the horoscope generator uses
        systems_to_test = [
            {'name': 'Європейська астрологія', 'position': 1},
            {'name': 'Китайська астрологія', 'position': 2},
            {'name': 'Індійська астрологія', 'position': 3},
            {'name': 'Лал Кітаб', 'position': 4},
            {'name': 'Джйотіш', 'position': 5},
            {'name': 'Нумерологія', 'position': 6},
            {'name': 'Таро', 'position': 7},
            {'name': 'Планетарна астрологія', 'position': 8},
        ]
        
        all_found = True
        
        for system in systems_to_test:
            # Use the corrected query (order instead of position)
            blog_block = BlogBlock.query.filter_by(order=system['position']).first()
            
            if blog_block:
                print(f"✅ Found block for {system['name']} (order={system['position']})")
                print(f"   Title: {blog_block.title}")
                print(f"   Active: {blog_block.is_active}")
            else:
                print(f"❌ No block found for {system['name']} (order={system['position']})")
                all_found = False
        
        if all_found:
            print("\n🎉 All blog blocks found successfully!")
            print("✅ The horoscope generator should now work without 'блок не найден' errors.")
        else:
            print("\n⚠️  Some blog blocks are missing. Run the block creation script first.")
            
        return all_found

if __name__ == "__main__":
    test_blog_blocks()
