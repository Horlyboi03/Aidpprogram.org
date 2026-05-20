"""
Migration script to add id_document_back_path column to applications table
Run this once: python add_id_back_column.py
"""
from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Check if column already exists
        result = db.session.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='applications' AND column_name='id_document_back_path'
        """))
        
        if result.fetchone() is None:
            # Add the column
            db.session.execute(text("""
                ALTER TABLE applications 
                ADD COLUMN id_document_back_path VARCHAR(500)
            """))
            db.session.commit()
            print("✓ Successfully added id_document_back_path column to applications table")
        else:
            print("✓ Column id_document_back_path already exists")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        db.session.rollback()
