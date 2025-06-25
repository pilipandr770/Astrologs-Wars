"""
Fix for horoscope display issues
"""
from app import create_app, db
from app.models import BlogBlock
import os

app = create_app()

with app.app_context():
    # First, let's check if all the blocks are active
    blocks = BlogBlock.query.all()
    print(f"Total blocks: {len(blocks)}")
    active_blocks = [b for b in blocks if b.is_active]
    print(f"Active blocks: {len(active_blocks)}")
    
    # Now, let's create a custom CSS file to fix any display issues
    custom_css = """
/* Fix for blog card display issues */
.blog-card, .card {
    display: block !important;
    visibility: visible !important;
}

.blog-section .row {
    display: flex;
    flex-wrap: wrap;
    width: 100%;
}

.blog-section .col {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
}
    """
    
    # Save the CSS file
    css_path = os.path.join(app.static_folder, 'css', 'fix_blog_display.css')
    with open(css_path, 'w') as f:
        f.write(custom_css)
    
    print(f"Created CSS fix at {css_path}")
    
    # Now, let's modify the base template to include our fix
    base_template_path = os.path.join(app.root_path, 'templates', 'base.html')
    
    try:
        with open(base_template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if our fix is already included
        if 'fix_blog_display.css' not in content:
            # Find the head section
            head_end = content.find('</head>')
            if head_end > 0:
                # Insert our CSS link before head end
                insert_css = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/fix_blog_display.css\') }}">\n  '
                new_content = content[:head_end] + insert_css + content[head_end:]
                
                # Save the modified template
                with open(base_template_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"Modified {base_template_path} to include fix")
            else:
                print(f"Could not find </head> in {base_template_path}")
        else:
            print(f"Fix already included in {base_template_path}")
            
    except Exception as e:
        print(f"Error modifying template: {str(e)}")
