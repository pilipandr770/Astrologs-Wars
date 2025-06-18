#!/usr/bin/env python3
"""
Script to check and display all blog blocks with their attributes.
"""
import os
from app import create_app, db
from app.models import BlogBlock, Block

def check_all_blocks():
    """Check all blocks in database"""
    # Clean DATABASE_URL to remove any newlines
    if 'DATABASE_URL' in os.environ:
        os.environ['DATABASE_URL'] = os.environ['DATABASE_URL'].strip()

    app = create_app()
    
    with app.app_context():
        print("📋 Checking all BlogBlock entries:")
        blog_blocks = BlogBlock.query.order_by(BlogBlock.position).all()
        
        for block in blog_blocks:
            print(f"ID: {block.id}, Position: {block.position}, Title: {block.title}, Active: {block.is_active}")
        
        print("\n📋 Checking all Block entries:")
        content_blocks = Block.query.order_by(Block.order).all()
        
        for block in content_blocks:
            print(f"ID: {block.id}, Order: {block.order}, Title: {block.title}, Active: {block.is_active}")

if __name__ == "__main__":
    check_all_blocks()
