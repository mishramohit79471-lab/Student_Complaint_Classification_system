-- Create database
CREATE DATABASE complaint_db;

-- Create user
CREATE USER complaint_user WITH PASSWORD 'complaint_user_123';

-- Grant privileges
ALTER ROLE complaint_user SET client_encoding TO 'utf8';
ALTER ROLE complaint_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE complaint_user SET default_transaction_deferrable TO on;
ALTER ROLE complaint_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE complaint_db TO complaint_user;

-- Connect to complaint_db and grant schema privileges
\c complaint_db
GRANT ALL ON SCHEMA public TO complaint_user;
