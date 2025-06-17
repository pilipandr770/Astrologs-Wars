#!/bin/bash
# setup_astro_blog_db.sh - Script to create all necessary tables in the astro_blog_db database

# Print what we're doing
echo "Setting up database tables for astro_blog_db on Render"

# Connect to the astro_blog_db database and create tables
# Note: We hide the password in output for security

DB_CONNECTION_STRING="postgresql://ittoken_db_user:Xm98VVSZv7cMJkopkdWRkgvZzC7Aly42@dpg-d0visga4d50c73ekmu4g-a.oregon-postgres.render.com/astro_blog_db"

# Extract components from the connection string for display
DB_USER=$(echo $DB_CONNECTION_STRING | sed -e 's/^postgresql:\/\/\([^:]*\):.*$/\1/')
DB_HOST=$(echo $DB_CONNECTION_STRING | sed -e 's/^postgresql:\/\/[^:]*:[^@]*@\(.*\)\/.*$/\1/')
DB_NAME=$(echo $DB_CONNECTION_STRING | sed -e 's/^.*\/\(.*\)$/\1/')

echo "Connecting to database $DB_NAME on $DB_HOST as user $DB_USER"

# Create the user table
echo "Creating user table..."
psql "$DB_CONNECTION_STRING" <<EOF
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) UNIQUE,
    password_hash VARCHAR(128),
    wallet_address VARCHAR(42),
    is_admin BOOLEAN DEFAULT FALSE,
    token_balance FLOAT DEFAULT 0.0
);
EOF

# Create the block table
echo "Creating block table..."
psql "$DB_CONNECTION_STRING" <<EOF
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
EOF

# Create the blog_block table
echo "Creating blog_block table..."
psql "$DB_CONNECTION_STRING" <<EOF
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
EOF

# Create the settings table
echo "Creating settings table..."
psql "$DB_CONNECTION_STRING" <<EOF
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
EOF

# Create the content_generation_log table
echo "Creating content_generation_log table..."
psql "$DB_CONNECTION_STRING" <<EOF
CREATE TABLE IF NOT EXISTS content_generation_log (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES blog_topic(id) ON DELETE SET NULL,
    action VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'success',
    message TEXT,
    created_at TIMESTAMP DEFAULT now(),
    duration_seconds FLOAT
);
EOF

# Create the autoposting_schedule table
echo "Creating autoposting_schedule table..."
psql "$DB_CONNECTION_STRING" <<EOF
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
EOF

# Create the image_storage table
echo "Creating image_storage table..."
psql "$DB_CONNECTION_STRING" <<EOF
CREATE TABLE IF NOT EXISTS image_storage (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) UNIQUE NOT NULL,
    binary_data BYTEA,
    content_type VARCHAR(128),
    created_at TIMESTAMP DEFAULT now()
);
EOF

# Add initial user (admin)
echo "Adding admin user..."
psql "$DB_CONNECTION_STRING" <<EOF
INSERT INTO "user" (username, password_hash, is_admin) 
VALUES ('admin', 'pbkdf2:sha256:260000$temporary_password_hash', TRUE)
ON CONFLICT (username) DO NOTHING;
EOF

# Add default settings
echo "Adding default settings..."
psql "$DB_CONNECTION_STRING" <<EOF
INSERT INTO settings (facebook, instagram, telegram, email)
VALUES ('https://facebook.com/', 'https://instagram.com/', 'https://t.me/', 'contact@example.com')
ON CONFLICT DO NOTHING;
EOF

# Add default autoposting schedule
echo "Adding default autoposting schedule..."
psql "$DB_CONNECTION_STRING" <<EOF
INSERT INTO autoposting_schedule (is_active, days_of_week, posting_time)
VALUES (FALSE, '1,3,5', '12:00')
ON CONFLICT DO NOTHING;
EOF

echo "Database setup complete!"

# Print out the table names and count
echo "Tables created:"
psql "$DB_CONNECTION_STRING" -c "\dt"

echo "Setup process completed successfully!"
