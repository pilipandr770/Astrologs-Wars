"""
A script to check the images of blog entries in the database
"""
from app import create_app
from app.models import BlogBlock
import os

app = create_app()

with app.app_context():
    blocks = BlogBlock.query.filter_by(is_active=True).order_by(BlogBlock.position).all()
    
    print(f'Total active blog entries: {len(blocks)}')
    
    uploads_dir = os.path.join(app.root_path, 'static', 'uploads', 'blog')
    print(f'Checking images in directory: {uploads_dir}')
    
    if os.path.exists(uploads_dir):
        files_in_dir = os.listdir(uploads_dir)
        print(f'Files in directory: {len(files_in_dir)}')
        print(', '.join(files_in_dir))
    else:
        print(f'Directory {uploads_dir} does not exist!')
    
    print('\nImage check for each block:')
    for block in blocks:
        if not block.featured_image:
            print(f'Block {block.position} ({block.title}) has no image set')
            continue
            
        image_path = os.path.join(uploads_dir, block.featured_image)
        exists = os.path.exists(image_path)
        print(f'Block {block.position} ({block.title}): {block.featured_image} - {"EXISTS" if exists else "MISSING"}')
