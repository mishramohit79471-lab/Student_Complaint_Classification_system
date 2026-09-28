#!/usr/bin/env python
"""
Script to create PostgreSQL database and user for the complaint system.
This connects to the default 'postgres' database as the postgres user.
"""
import sys
from sqlalchemy import create_engine, text

# Connection to default postgres database (using psycopg2)
# Try different password options
possible_urls = [
    "postgresql+psycopg2://postgres@localhost:5432/postgres",  # No password
    "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres",  # Password: postgres
    "postgresql+psycopg2://postgres:@localhost:5432/postgres",  # Empty password
]
default_db_url = possible_urls[0]  # Start with no password

# Target database and user
db_name = "complaint_db"
db_user = "complaint_user"
db_password = "complaint_user_123"
db_host = "localhost"
db_port = "5432"

try:
    # Connect to default postgres database
    print("Connecting to PostgreSQL as admin...")

    # Try connecting with the first URL
    engine = None
    for i, url in enumerate(possible_urls, 1):
        try:
            engine = create_engine(url)
            with engine.connect() as test_conn:
                test_conn.execute(text("SELECT 1"))
            print(f"✓ Connected successfully (attempt {i})")
            default_db_url = url
            break
        except Exception as e:
            if i < len(possible_urls):
                print(f"  Attempt {i} failed: {str(e)[:50]}... trying next...")
                continue
            else:
                raise Exception(f"Failed to connect to PostgreSQL with any credential: {e}")

    if engine is None:
        raise Exception("Could not connect to PostgreSQL")

    with engine.connect() as conn:
        # Disable autocommit for CREATE DATABASE
        conn.connection.autocommit = True

        # Drop existing database if it exists
        print(f"Checking if database '{db_name}' exists...")
        try:
            conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
            print(f"Dropped existing database '{db_name}'")
        except Exception as e:
            print(f"Database doesn't exist or couldn't be dropped: {e}")

        # Drop existing user if it exists
        print(f"Checking if user '{db_user}' exists...")
        try:
            conn.execute(text(f"DROP USER IF EXISTS {db_user}"))
            print(f"Dropped existing user '{db_user}'")
        except Exception as e:
            print(f"User doesn't exist or couldn't be dropped: {e}")

        # Create user
        print(f"Creating user '{db_user}'...")
        conn.execute(text(f"CREATE USER {db_user} WITH PASSWORD '{db_password}'"))
        print(f"✓ User '{db_user}' created")

        # Create database
        print(f"Creating database '{db_name}'...")
        conn.execute(text(f"CREATE DATABASE {db_name} OWNER {db_user}"))
        print(f"✓ Database '{db_name}' created")

        # Grant privileges
        print("Granting privileges...")
        conn.execute(text(f"ALTER USER {db_user} SET client_encoding TO 'utf8'"))
        conn.execute(text(f"ALTER USER {db_user} SET default_transaction_isolation TO 'read committed'"))
        conn.execute(text(f"ALTER USER {db_user} SET timezone TO 'UTC'"))
        print("✓ User configured")

    print("\n" + "="*50)
    print("DATABASE SETUP COMPLETE ✓")
    print("="*50)
    print(f"\nDatabase: {db_name}")
    print(f"User: {db_user}")
    print(f"Password: {db_password}")
    print(f"Host: {db_host}:{db_port}")
    print(f"\nConnection URL:")
    print(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Ensure PostgreSQL is running")
    print("2. Ensure default postgres user has password 'postgres'")
    print("   (or modify the connection string above)")
    print("3. Check PostgreSQL logs for errors")
    sys.exit(1)
