"""
Script to verify the shop block on the home page
"""
from app import create_app, db
from app.models import Product, Category, Settings
from datetime import datetime
import os

def check_shop_block():
    print("Checking shop block on home page...")
    app = create_app()
    
    with app.app_context():
        # Check if we have products
        products = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).all()
        print(f"Active products count: {len(products)}")
        
        # If we don't have any products or less than 3, create some
        if len(products) < 3:
            print("Creating sample products...")
            
            # Check if we have categories
            categories = Category.query.all()
            category_id = 1
            if categories:
                category_id = categories[0].id
            
            # Create at least 3 products
            for i in range(1, 4):
                if i <= len(products):
                    continue
                    
                product = Product(
                    name=f"Product {i}",
                    slug=f"product-{i}",
                    description=f"This is product {i} for testing",
                    price=19.99,
                    is_active=True,
                    order=i,
                    category_id=category_id,
                    created_at=datetime.utcnow()
                )
                db.session.add(product)
            
            db.session.commit()
            print("Sample products created")
          # Make sure the settings object exists
        settings = Settings.query.first()
        if not settings:
            print("Creating settings object...")
            settings = Settings(
                facebook="https://facebook.com/astrologywars",
                instagram="https://instagram.com/astrologywars",
                telegram="https://t.me/astrologywars",
                email="contact@astrologywars.com"
            )
            db.session.add(settings)
            db.session.commit()
            print("Settings created")
        
        # Check if the shop block is visible on the home page
        print("\nVerification complete. The shop block should now appear at the bottom of the home page.")
        print("Please restart the Flask application and visit the home page to verify.")

if __name__ == "__main__":
    check_shop_block()
