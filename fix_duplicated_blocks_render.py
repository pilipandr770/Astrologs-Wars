#!/usr/bin/env python3
"""
Script to fix the duplication of content blocks on the index page for Render environment.
This script will deactivate the Block entries with order 1-8 that duplicate the BlogBlock content.

Usage on Render:
python fix_duplicated_blocks_render.py
"""
import os
from app import create_app, db
from app.models import Block

def fix_duplicated_blocks():
    """Deactivate duplicate Block entries"""
    # Clean DATABASE_URL to remove any newlines
    if 'DATABASE_URL' in os.environ:
        os.environ['DATABASE_URL'] = os.environ['DATABASE_URL'].strip()

    app = create_app()
    
    with app.app_context():
        print("🔧 Deactivating duplicate horoscope Block entries (order 1-8):")
        
        # Find blocks with order 1-8
        for order_num in range(1, 9):
            block = Block.query.filter_by(order=order_num).first()
            if block:
                # If the block exists and is active, deactivate it
                if block.is_active:
                    block.is_active = False
                    print(f"✅ Block {block.id} (Order: {block.order}, Title: {block.title}) deactivated")
                else:
                    print(f"ℹ️ Block {block.id} (Order: {block.order}, Title: {block.title}) already inactive")
        
        # Commit changes
        db.session.commit()
        print("✅ Changes committed to database")
        
        # Verify changes
        print("\n📋 Verification - Block entries status:")
        blocks = Block.query.order_by(Block.order).all()
        for block in blocks:
            status = "✓ Inactive" if not block.is_active else "✗ Still active"
            print(f"ID: {block.id}, Order: {block.order}, Title: {block.title}, Status: {status}")

if __name__ == "__main__":
    fix_duplicated_blocks()
