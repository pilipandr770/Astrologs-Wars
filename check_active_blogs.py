"""
A script to check the active status of blog entries in the database
"""
from app import create_app
from app.models import BlogBlock

app = create_app()

with app.app_context():
    all_blocks = BlogBlock.query.all()
    active_blocks = BlogBlock.query.filter_by(is_active=True).all()
    
    print(f'Total blog entries: {len(all_blocks)}')
    print(f'Active blog entries: {len(active_blocks)}')
    
    print('\nActive blocks:')
    for block in active_blocks:
        print(f'ID: {block.id}, Position: {block.position}, Title: {block.title}')
    
    print('\nInactive blocks:')
    inactive_blocks = [b for b in all_blocks if not b.is_active]
    for block in inactive_blocks:
        print(f'ID: {block.id}, Position: {block.position}, Title: {block.title}')
