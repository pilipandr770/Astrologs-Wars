"""
A script to render and display the generated HTML content
"""
from app import create_app
from app.models import BlogBlock
from flask import render_template, g
from app.blog.routes import get_blog_block_title, get_blog_block_summary

app = create_app()

with app.app_context():
    g.lang = 'uk'  # Set default language
    
    # Get all active blocks
    blocks = BlogBlock.query.filter_by(is_active=True).order_by(BlogBlock.position).all()
    
    # Render the template to HTML
    html_content = render_template(
        'blog/index.html', 
        blocks=blocks,
        get_blog_block_title=get_blog_block_title,
        get_blog_block_summary=get_blog_block_summary,
        get_blog_block_content=lambda x: ""  # Dummy function
    )
    
    # Save HTML to file
    with open('blog_rendered.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML rendered with {len(blocks)} blocks and saved to blog_rendered.html")
    
    # Print block information for verification
    print("\nBlocks being rendered:")
    for i, block in enumerate(blocks, 1):
        print(f"{i}. Position: {block.position}, Title: {block.title}, Image: {block.featured_image or 'None'}")
