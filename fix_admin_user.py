#!/usr/bin/env python3
"""
Script to update the password_hash column size and recreate admin user.
This handles the database schema change and user creation in one step.
"""
import os
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
from sqlalchemy import text

def update_password_column_and_create_admin():
    """Update password_hash column size and create admin user"""    # Clean DATABASE_URL to remove any newlines
    if 'DATABASE_URL' in os.environ:
        os.environ['DATABASE_URL'] = os.environ['DATABASE_URL'].strip()

    app = create_app()
    
    with app.app_context():
        print("🔧 Updating password_hash column size...")
        
        try:
            # First, try to alter the column size
            with db.engine.connect() as connection:
                connection.execute(text("ALTER TABLE \"user\" ALTER COLUMN password_hash TYPE VARCHAR(255)"))
                connection.commit()
            print("✅ Successfully updated password_hash column to VARCHAR(255)")
        except Exception as e:
            print(f"⚠️  Column update failed (might already be correct size): {str(e)}")
        
        print("🔄 Creating/updating admin user...")
        
        # Remove existing admin user if exists
        existing_user = User.query.filter_by(username='andrii770').first()
        if existing_user:
            db.session.delete(existing_user)
            print("🗑️  Removed existing admin user")
          # Create password hash with fallback for different environments
        try:
            # Try scrypt first (preferred for production)
            password_hash = generate_password_hash('4517710070', method='scrypt')
            print(f"🔑 Generated scrypt password hash (length: {len(password_hash)})")
        except ValueError:
            # Fall back to pbkdf2 if scrypt is not available (local development)
            password_hash = generate_password_hash('4517710070', method='pbkdf2:sha256')
            print(f"🔑 Generated pbkdf2 password hash (length: {len(password_hash)})")
        
        # Create new admin user
        admin_user = User(
            username='andrii770',
            password_hash=password_hash,
            is_admin=True,
            token_balance=0.0
        )
        
        db.session.add(admin_user)
        
        try:
            db.session.commit()
            print("✅ Admin user created successfully!")
            
            # Verify the user was created
            user_check = User.query.filter_by(username='andrii770').first()
            if user_check:
                print(f"✅ Verification: User '{user_check.username}' exists with admin={user_check.is_admin}")
            else:
                print("❌ Verification failed: User not found")
                
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating admin user: {str(e)}")
            return False
            
        return True

if __name__ == "__main__":
    success = update_password_column_and_create_admin()
    if success:
        print("\n🎉 Admin user setup completed successfully!")
    else:
        print("\n❌ Admin user setup failed!")
