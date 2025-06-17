"""
A script to check the blog entries in the database
"""
from app import create_app
from app.models import BlogBlock

app = create_app()

with app.app_context():
    blocks = BlogBlock.query.all()
    print(f'Total blog entries: {len(blocks)}')
    for block in blocks:
        print(f'ID: {block.id}, Title: {block.title}, Position: {block.position}')
        print(f'Has content: {"Yes" if block.content else "No"}, Has summary: {"Yes" if block.summary else "No"}')
        print(f'Image: {block.featured_image}')
        print('-' * 80)
