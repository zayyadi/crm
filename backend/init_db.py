
"""
Database initialization script for the CRM system.
This script creates all necessary database tables.
"""

import asyncio
import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import db, Base
from app.core.config import settings

async def init_db():
    """Initialize the database and create all tables."""
    print("Initializing database...")
    
    try:
        
        db.init()
        
        
        async with db._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("Database initialized successfully!")
        return True
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

if __name__ == "__main__":
    
    result = asyncio.run(init_db())
    
    if not result:
        sys.exit(1)
