"""
Database migration: Add is_delivered column to messages table
Run this script once to update the database schema.
"""
from app import create_app, db
from sqlalchemy import text

def add_is_delivered_column():
    """Add is_delivered column to messages table if it doesn't exist."""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if column already exists (PostgreSQL)
            result = db.session.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_name='messages' 
                AND column_name='is_delivered'
            """))
            column_exists = result.scalar() > 0
            
            if column_exists:
                print("✓ Column 'is_delivered' already exists in messages table")
                return
            
            # Add the column (PostgreSQL)
            db.session.execute(text(
                "ALTER TABLE messages ADD COLUMN is_delivered BOOLEAN DEFAULT FALSE"
            ))
            db.session.commit()
            print("✓ Successfully added 'is_delivered' column to messages table")
            
            # Update existing messages to mark them as delivered
            db.session.execute(text(
                "UPDATE messages SET is_delivered = TRUE WHERE is_delivered IS NULL"
            ))
            db.session.commit()
            print("✓ Updated existing messages to mark as delivered")
            
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error adding column: {e}")
            raise

if __name__ == '__main__':
    print("=" * 60)
    print("Database Migration: Add is_delivered column")
    print("=" * 60)
    add_is_delivered_column()
    print("=" * 60)
    print("Migration complete!")
    print("=" * 60)
