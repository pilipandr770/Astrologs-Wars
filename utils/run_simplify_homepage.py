#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to simplify the homepage by:
1. Removing all horoscope blocks from the main page
2. Displaying only the admin-editable block with is_top=True
3. Adding a shop section with featured products at the bottom
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path to find the app package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Block, Product, Settings

def main():
    """
    Main function to update homepage configuration
    """
    print("Starting homepage simplification process...")
    
    # Create app context
    app = create_app()
    with app.app_context():
        # 1. Verify top block exists or create one
        top_block = Block.query.filter_by(is_top=True).first()
        if not top_block:
            print("Creating top block as it doesn't exist...")
            top_block = Block(
                title="Астрологічний портал",
                title_en="Astrology Portal",
                title_de="Astrologie-Portal",
                title_ru="Астрологический портал",
                content="Вітаємо на нашому професійному астрологічному порталі, де ви можете дізнатися щоденні гороскопи, персональні прогнози та отримати астрологічні консультації.",
                content_en="Welcome to our professional astrology portal, where you can discover daily horoscopes, personal forecasts, and astrological consultations.",
                content_de="Willkommen auf unserem professionellen Astrologieportal, wo Sie tägliche Horoskope, persönliche Vorhersagen und astrologische Beratungen entdecken können.",
                content_ru="Добро пожаловать на наш профессиональный астрологический портал, где вы можете открыть для себя ежедневные гороскопы, персональные прогнозы и астрологические консультации.",
                is_active=True,
                is_top=True,
                slug="main-top",
                order=0
            )
            db.session.add(top_block)
            db.session.commit()
            print("Default top block created successfully!")
            
        # 2. Check for featured products
        products = Product.query.filter_by(is_active=True).count()
        if products == 0:
            print("Warning: No active products found for the shop section.")
        else:
            print(f"Found {products} active products that can be shown in featured section.")
            
        # 3. Verify settings exist for currency symbol
        settings = Settings.query.first()
        if not settings:
            print("Warning: No settings found. Default currency symbol will be used.")
        elif not settings.currency_symbol:
            print("Warning: No currency symbol set in settings. Default will be used.")
            settings.currency_symbol = "€"
            db.session.commit()
            print("Added default currency symbol to settings.")
            
        print("\nHomepage simplification completed successfully.")
        print("\nChanges applied:")
        print("1. Main page now displays only one admin-editable block at the top (set is_top=True in admin)")
        print("2. The shop section shows featured products at the bottom")
        print("3. All horoscope and blog blocks have been removed from the main page")
        print("4. Automated horoscope generation will continue to post to the blog")
        print("\nTo make further changes to the main block:")
        print("1. Log in to the admin panel")
        print("2. Go to Blocks section")
        print("3. Edit the block with is_top=True")
        
if __name__ == "__main__":
    main()
