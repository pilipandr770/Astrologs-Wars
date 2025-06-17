"""
A script to print out the HTML structure of blog entries without using Flask templates
"""
from app import create_app
from app.models import BlogBlock
import os

app = create_app()

def strip_html(text):
    """Simple function to remove HTML tags for display purposes"""
    if not text:
        return ""
    # Very basic HTML tag removal for display purposes
    import re
    return re.sub(r'<.*?>', '', text)

with app.app_context():
    blocks = BlogBlock.query.filter_by(is_active=True).order_by(BlogBlock.position).all()
    print(f"Found {len(blocks)} active blog blocks\n")
    
    # Print HTML structure of each block
    for i, block in enumerate(blocks[:8], 1):  # Only show the first 8 blocks
        print(f"Block {i}: {block.title}")
        print(f"Position: {block.position}")
        print(f"Image: {block.featured_image or 'None'}")
        print(f"Summary: {strip_html(block.summary)[:100]}..." if block.summary else "No summary")
        # Print HTML that would be rendered
        print("\nHTML structure that would be generated:")
        print(f'''<div class="col">
    <div class="card h-100 shadow-sm">
        <img src="/static/uploads/blog/{block.featured_image}" 
             class="card-img-top" style="height: 200px; object-fit: cover;" 
             alt="{block.title}">
        <div class="card-body">
            <h3 class="card-title h5">{block.title}</h3>
            <p class="card-text">{strip_html(block.summary)[:50]}...</p>
        </div>
        <div class="card-footer bg-white border-0">
            <a href="/blog/{block.position}" class="btn btn-outline-primary">
                Читати далі
            </a>
        </div>
    </div>
</div>''')
        print("-" * 80)
