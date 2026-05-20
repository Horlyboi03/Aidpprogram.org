"""
Database Migration: Add image_url column to messages table
Run this script once to add the image_url column for image sharing in chat.
"""
from app import create_app, db
from sqlalchemy import text

app = create_app()

def add_image_url_column():
    with app.app_context():
        try:
            print("=" * 60)
            print("Database Migration: Add image_url column")
            print("=" * 60)
            
            # Check if column already exists (PostgreSQL)
            result = db.session.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_name='messages' AND column_name='image_url'
            """))
            exists = result.scalar() > 0
            
            if exists:
                print("✓ Column 'image_url' already exists in messages table")
            else:
                print("Adding 'image_url' column to messages table...")
                db.session.execute(text("""
                    ALTER TABLE messages 
                    ADD COLUMN image_url VARCHAR(500)
                """))
                db.session.commit()
                print("✓ Column 'image_url' added successfully")
            
            print("=" * 60)
            print("Migration completed successfully!")
            print("=" * 60)
            
        except Exception as e:
            print(f"✗ Error adding column: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    add_image_url_column()
