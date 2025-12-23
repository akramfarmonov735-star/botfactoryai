"""
Database Migration Script for Mini App
Run this after deploying to add new columns to PostgreSQL
"""

import os
import sys

def run_migration():
    """Add Mini App columns to existing database"""
    
    # Get database URL from environment
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("ERROR: DATABASE_URL not set")
        return 1
    
    # Determine database type
    is_postgres = 'postgresql' in database_url or 'postgres' in database_url
    
    if is_postgres:
        import psycopg2
        
        # Fix postgres:// to postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Add columns to bot table
        columns = [
            ("business_type", "VARCHAR(20) DEFAULT 'product'"),
            ("business_description", "VARCHAR(500)"),
            ("business_logo", "VARCHAR(500)"),
            ("working_hours", "VARCHAR(100)"),
            ("miniapp_enabled", "BOOLEAN DEFAULT true"),
            ("description", "VARCHAR(500)"),
        ]
        
        for col_name, col_def in columns:
            try:
                cursor.execute(f"ALTER TABLE bot ADD COLUMN IF NOT EXISTS {col_name} {col_def}")
                print(f"✅ Added/verified column: bot.{col_name}")
            except Exception as e:
                print(f"⚠️ Column bot.{col_name}: {e}")
        
        # Create MiniAppOrder table
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mini_app_order (
                    id SERIAL PRIMARY KEY,
                    bot_id INTEGER NOT NULL REFERENCES bot(id),
                    customer_name VARCHAR(200) NOT NULL,
                    customer_phone VARCHAR(50) NOT NULL,
                    customer_address VARCHAR(500),
                    note TEXT,
                    items TEXT NOT NULL,
                    total_amount FLOAT DEFAULT 0,
                    telegram_user_id VARCHAR(50),
                    status VARCHAR(20) DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ Created/verified table: mini_app_order")
        except Exception as e:
            print(f"⚠️ Table mini_app_order: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
    else:
        # SQLite
        import sqlite3
        
        db_path = database_url.replace('sqlite:///', '')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        columns = [
            ("business_type", "VARCHAR(20)", "'product'"),
            ("business_description", "VARCHAR(500)", None),
            ("business_logo", "VARCHAR(500)", None),
            ("working_hours", "VARCHAR(100)", None),
            ("miniapp_enabled", "BOOLEAN", "1"),
            ("description", "VARCHAR(500)", None),
        ]
        
        for col_name, col_type, default in columns:
            try:
                if default:
                    cursor.execute(f"ALTER TABLE bot ADD COLUMN {col_name} {col_type} DEFAULT {default}")
                else:
                    cursor.execute(f"ALTER TABLE bot ADD COLUMN {col_name} {col_type}")
                print(f"✅ Added column: bot.{col_name}")
            except Exception as e:
                print(f"⚠️ Column bot.{col_name}: already exists or error")
        
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mini_app_order (
                    id INTEGER PRIMARY KEY,
                    bot_id INTEGER NOT NULL,
                    customer_name VARCHAR(200) NOT NULL,
                    customer_phone VARCHAR(50) NOT NULL,
                    customer_address VARCHAR(500),
                    note TEXT,
                    items TEXT NOT NULL,
                    total_amount FLOAT DEFAULT 0,
                    telegram_user_id VARCHAR(50),
                    status VARCHAR(20) DEFAULT 'pending',
                    created_at DATETIME,
                    updated_at DATETIME,
                    FOREIGN KEY (bot_id) REFERENCES bot (id)
                )
            """)
            print("✅ Created/verified table: mini_app_order")
        except Exception as e:
            print(f"⚠️ Table mini_app_order: {e}")
        
        conn.commit()
        conn.close()
    
    print("\n✅ Migration completed successfully!")
    return 0


if __name__ == '__main__':
    sys.exit(run_migration())
