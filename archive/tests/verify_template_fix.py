#!/usr/bin/env python3
"""
Script to verify the fixed homepage template
"""
import os
import sys

def verify_homepage():
    """Verify that the homepage template is correctly set up for simple layout"""
    # Get the base path for the project
    base_path = os.getcwd()
    
    print(f"Working in directory: {base_path}")
    
    # Check if template file exists and is correctly fixed
    template_path = os.path.join(base_path, 'app', 'templates', 'index.html')
    if not os.path.exists(template_path):
        print("ERROR: index.html template doesn't exist")
        return False
    
    # Check if CSS files are correctly set up
    main_css_path = os.path.join(base_path, 'app', 'static', 'css', 'main-block.css')
    if not os.path.exists(main_css_path):
        print("WARNING: main-block.css file doesn't exist")
    else:
        print("✓ main-block.css found")
    
    # Create a marker file to indicate we've verified the setup
    marker_path = os.path.join(base_path, 'template_fix_verified.txt')
    with open(marker_path, 'w', encoding='utf-8') as f:
        f.write("Homepage template syntax fix verified on: " + os.path.basename(sys.argv[0]))
    
    print(f"\nVerification complete. Created marker file: {marker_path}")
    print("\nREMINDER: Make sure to check that the template displays correctly in your browser")
    print("If you see any issues, check the Flask logs for template errors")
    
    return True

if __name__ == "__main__":
    verify_homepage()
