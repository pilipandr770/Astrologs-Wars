#!/bin/bash
# create_and_setup_db.sh - Create and set up the database on Render

# Database connection details
DB_USER="ittoken_db_user"
DB_PASS="Xm98VVSZv7cMJkopkdWRkgvZzC7Aly42"
DB_HOST="dpg-d0visga4d50c73ekmu4g-a.oregon-postgres.render.com"
DB_PORT="5432"

# First, connect to the default 'postgres' database to create our database
echo "Connecting to default postgres database..."
PGPASSWORD="$DB_PASS" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres << EOF
-- Check if database exists and create it if it doesn't
SELECT 'CREATE DATABASE astro_blog_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'astro_blog_db')\gexec
EOF

# Now connect to our newly created database and create the tables
echo "Connecting to astro_blog_db to create tables..."
PGPASSWORD="$DB_PASS" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d astro_blog_db << EOF
-- Create user table
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) UNIQUE,
    password_hash VARCHAR(128),
    wallet_address VARCHAR(42),
    is_admin BOOLEAN DEFAULT FALSE,
    token_balance FLOAT DEFAULT 0.0
);

-- Create block table
CREATE TABLE IF NOT EXISTS block (
    id SERIAL PRIMARY KEY,
    title VARCHAR(128),
    content TEXT,
    image VARCHAR(256),
    "order" INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    slug VARCHAR(64) UNIQUE,
    is_top BOOLEAN DEFAULT FALSE,
    title_ua VARCHAR(128),
    title_en VARCHAR(128),
    title_de VARCHAR(128),
    title_ru VARCHAR(128),
    content_ua TEXT,
    content_en TEXT,
    content_de TEXT,
    content_ru TEXT
);

-- Create blog_topic table
CREATE TABLE IF NOT EXISTS blog_topic (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    title_ua VARCHAR(128),
    title_en VARCHAR(128),
    title_de VARCHAR(128),
    title_ru VARCHAR(128),
    description_ua TEXT,
    description_en TEXT,
    description_de TEXT,
    description_ru TEXT,
    status VARCHAR(32),
    created_at TIMESTAMP DEFAULT now(),
    scheduled_for TIMESTAMP,
    blog_block_id INTEGER
);

-- Create blog_block table
CREATE TABLE IF NOT EXISTS blog_block (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    featured_image VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    position INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    title_ua VARCHAR(255),
    title_en VARCHAR(255),
    title_de VARCHAR(255),
    title_ru VARCHAR(255),
    content_ua TEXT,
    content_en TEXT,
    content_de TEXT,
    content_ru TEXT,
    summary_ua TEXT,
    summary_en TEXT,
    summary_de TEXT,
    summary_ru TEXT
);

-- Create astro_blog_post table
CREATE TABLE IF NOT EXISTS astro_blog_post (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    slug VARCHAR(255),
    content TEXT,
    summary TEXT,
    featured_image VARCHAR(255),
    is_published BOOLEAN,
    is_featured BOOLEAN,
    publish_date TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    title_ua VARCHAR(255),
    title_en VARCHAR(255),
    title_de VARCHAR(255),
    title_ru VARCHAR(255),
    content_ua TEXT,
    content_en TEXT,
    content_de TEXT,
    content_ru TEXT,
    summary_ua TEXT,
    summary_en TEXT,
    summary_de TEXT,
    summary_ru TEXT,
    is_auto_generated BOOLEAN,
    topic_id INTEGER,
    telegram_post_id VARCHAR(128),
    other_platform_links JSON
);

-- Create settings table
CREATE TABLE IF NOT EXISTS settings (
    id SERIAL PRIMARY KEY,
    facebook VARCHAR(256),
    instagram VARCHAR(256),
    telegram VARCHAR(256),
    email VARCHAR(256),
    contract_address VARCHAR(42),
    token_name VARCHAR(64),
    token_symbol VARCHAR(10),
    network_rpc VARCHAR(256),
    network_chain_id INTEGER DEFAULT 80001
);

-- Create autoposting_schedule table
CREATE TABLE IF NOT EXISTS autoposting_schedule (
    id SERIAL PRIMARY KEY,
    is_active BOOLEAN DEFAULT FALSE,
    days_of_week VARCHAR(20) DEFAULT '0,1,2,3,4,5,6',
    posting_time VARCHAR(5) DEFAULT '12:00',
    auto_translate BOOLEAN DEFAULT TRUE,
    target_languages VARCHAR(50) DEFAULT 'en,de,ru',
    generate_images BOOLEAN DEFAULT TRUE,
    image_style VARCHAR(100) DEFAULT 'professional, high quality',
    post_to_telegram BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- Create content_generation_log table
CREATE TABLE IF NOT EXISTS content_generation_log (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER,
    action VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'success',
    message TEXT,
    created_at TIMESTAMP DEFAULT now(),
    duration_seconds FLOAT
);

-- Add foreign key reference
ALTER TABLE blog_topic ADD CONSTRAINT fk_blog_block 
    FOREIGN KEY (blog_block_id) REFERENCES blog_block(id) ON DELETE SET NULL;

ALTER TABLE content_generation_log ADD CONSTRAINT fk_topic_id
    FOREIGN KEY (topic_id) REFERENCES blog_topic(id) ON DELETE SET NULL;

-- Insert default admin user
INSERT INTO "user" (username, password_hash, is_admin)
VALUES ('admin', 'pbkdf2:sha256:260000$temporary_password_hash', TRUE)
ON CONFLICT (username) DO NOTHING;

-- Insert default settings
INSERT INTO settings (facebook, instagram, telegram, email)
VALUES ('https://facebook.com/', 'https://instagram.com/', 'https://t.me/', 'contact@example.com')
ON CONFLICT DO NOTHING;

-- Insert default autoposting schedule
INSERT INTO autoposting_schedule (is_active, days_of_week, posting_time)
VALUES (FALSE, '1,3,5', '12:00')
ON CONFLICT DO NOTHING;

-- List the tables we created
\dt
EOF

# Show success message
echo "Database and tables setup complete! Please update your Render configuration to use the astro_blog_db database."
