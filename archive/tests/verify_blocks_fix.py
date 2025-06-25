#!/usr/bin/env python3
"""
Script to verify that blocks are no longer duplicated on the index page.
"""
import os
from app import create_app, db
from app.models import BlogBlock, Block
from flask import render_template

def verify_blocks_fix():
    """Verify that blocks are no longer duplicated on index page"""
    # Clean DATABASE_URL to remove any newlines
    if 'DATABASE_URL' in os.environ:
        os.environ['DATABASE_URL'] = os.environ['DATABASE_URL'].strip()

    app = create_app()
    
    with app.app_context():
        print("📋 Verifying blocks for the index page:")
        
        # Check Block entries (should all be inactive for positions 1-8)
        content_blocks = Block.query.filter_by(is_active=True).order_by(Block.order).all()
        print(f"\n✅ Active Block entries: {len(content_blocks)}")
        for block in content_blocks:
            print(f"ID: {block.id}, Order: {block.order}, Title: {block.title}")
        
        # Check BlogBlock entries (these should be active for positions 1-8)
        blog_blocks = BlogBlock.query.filter_by(is_active=True).filter(BlogBlock.position <= 8).order_by(BlogBlock.position).all()
        print(f"\n✅ Active BlogBlock entries (positions 1-8): {len(blog_blocks)}")
        for block in blog_blocks:
            print(f"ID: {block.id}, Position: {block.position}, Title: {block.title}")
        
        # Check the recent_blog_blocks variable that's passed to the template
        recent_blog_blocks = BlogBlock.query.filter_by(is_active=True).order_by(BlogBlock.position).limit(7).all()
        print(f"\n✅ recent_blog_blocks variable (limit 7): {len(recent_blog_blocks)}")
        for block in recent_blog_blocks:
            print(f"ID: {block.id}, Position: {block.position}, Title: {block.title}")
            
        # Verification summary
        print("\n📊 VERIFICATION SUMMARY:")
        print(f"- Active Block entries for positions 1-8: {len([b for b in Block.query.filter_by(is_active=True).all() if b.order <= 8])}")
        print(f"- Active BlogBlock entries for positions 1-8: {len(blog_blocks)}")
        
        if len([b for b in Block.query.filter_by(is_active=True).all() if b.order <= 8]) == 0 and len(blog_blocks) > 0:
            print("\n✅ FIX SUCCESSFUL: No more duplicated blocks on the index page!")
        else:
            print("\n❌ FIX INCOMPLETE: There might still be duplicated blocks!")

if __name__ == "__main__":
    verify_blocks_fix()
