-- PostgreSQL DDL for Astrolog Wars
-- Generated SQL statements to create all database tables for deployment on Render

-- Users Table
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) UNIQUE,
    password_hash VARCHAR(128),
    wallet_address VARCHAR(42),
    is_admin BOOLEAN DEFAULT FALSE,
    token_balance FLOAT DEFAULT 0.0
);

-- Blocks Table (Content blocks for site sections)
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

-- Payment Methods
CREATE TABLE IF NOT EXISTS payment_method (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64),
    type VARCHAR(32),
    details JSONB,
    qr_code VARCHAR(256),
    name_ua VARCHAR(64),
    name_en VARCHAR(64),
    name_de VARCHAR(64),
    name_ru VARCHAR(64),
    description_ua TEXT,
    description_en TEXT,
    description_de TEXT,
    description_ru TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    "order" INTEGER DEFAULT 1,
    invoice_pdf VARCHAR(256)
);

-- Payments
CREATE TABLE IF NOT EXISTS payment (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(128),
    email VARCHAR(128),
    phone VARCHAR(32),
    amount FLOAT,
    method_id INTEGER REFERENCES payment_method(id),
    status VARCHAR(32) DEFAULT 'pending',
    payment_info JSONB,
    invoice_pdf VARCHAR(256),
    proof_image VARCHAR(256),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- Settings
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

-- Categories
CREATE TABLE IF NOT EXISTS category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64),
    slug VARCHAR(64) UNIQUE,
    description TEXT,
    image VARCHAR(256),
    is_active BOOLEAN DEFAULT TRUE,
    "order" INTEGER DEFAULT 1,
    name_ua VARCHAR(64),
    name_en VARCHAR(64),
    name_de VARCHAR(64),
    name_ru VARCHAR(64),
    description_ua TEXT,
    description_en TEXT,
    description_de TEXT,
    description_ru TEXT
);

-- Products
CREATE TABLE IF NOT EXISTS product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128),
    slug VARCHAR(128) UNIQUE,
    description TEXT,
    image VARCHAR(256),
    price FLOAT,
    token_price FLOAT,
    is_digital BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    category_id INTEGER REFERENCES category(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    name_ua VARCHAR(128),
    name_en VARCHAR(128),
    name_de VARCHAR(128),
    name_ru VARCHAR(128),
    description_ua TEXT,
    description_en TEXT,
    description_de TEXT,
    description_ru TEXT,
    example_url VARCHAR(512),
    features JSONB,
    delivery_time VARCHAR(128),
    support_period VARCHAR(128)
);

-- Product Images
CREATE TABLE IF NOT EXISTS product_image (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES product(id) ON DELETE CASCADE,
    image_path VARCHAR(256),
    title VARCHAR(128),
    description TEXT,
    "order" INTEGER DEFAULT 1,
    is_main BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- Shopping Cart
CREATE TABLE IF NOT EXISTS cart (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Cart Items
CREATE TABLE IF NOT EXISTS cart_item (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER REFERENCES cart(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES product(id),
    quantity INTEGER DEFAULT 1
);

-- Orders
CREATE TABLE IF NOT EXISTS "order" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id),
    status VARCHAR(32) DEFAULT 'pending',
    total_price FLOAT,
    payment_type VARCHAR(32),
    payment_id INTEGER REFERENCES payment(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITHOUT TIME ZONE
);

-- Order Items
CREATE TABLE IF NOT EXISTS order_item (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES "order"(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES product(id),
    quantity INTEGER DEFAULT 1,
    price FLOAT
);

-- Token Information
CREATE TABLE IF NOT EXISTS token (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64),
    symbol VARCHAR(10),
    contract_address VARCHAR(42),
    decimals INTEGER DEFAULT 18,
    total_supply FLOAT,
    circulating_supply FLOAT,
    token_price_usd FLOAT,
    description TEXT,
    description_ua TEXT,
    description_en TEXT,
    description_de TEXT,
    description_ru TEXT
);

-- Airdrops
CREATE TABLE IF NOT EXISTS airdrop (
    id SERIAL PRIMARY KEY,
    title VARCHAR(128),
    description TEXT,
    total_amount FLOAT,
    amount_per_user FLOAT,
    start_date TIMESTAMP WITHOUT TIME ZONE,
    end_date TIMESTAMP WITHOUT TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    title_ua VARCHAR(128),
    title_en VARCHAR(128),
    title_de VARCHAR(128),
    title_ru VARCHAR(128),
    description_ua TEXT,
    description_en TEXT,
    description_de TEXT,
    description_ru TEXT
);

-- Airdrop Participations
CREATE TABLE IF NOT EXISTS airdrop_participation (
    id SERIAL PRIMARY KEY,
    airdrop_id INTEGER REFERENCES airdrop(id),
    user_id INTEGER REFERENCES "user"(id),
    wallet_address VARCHAR(42),
    amount FLOAT,
    status VARCHAR(32) DEFAULT 'pending',
    tx_hash VARCHAR(66),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- Token Sales
CREATE TABLE IF NOT EXISTS token_sale (
    id SERIAL PRIMARY KEY,
    title VARCHAR(128),
    description TEXT,
    total_amount FLOAT,
    price FLOAT,
    min_purchase FLOAT,
    max_purchase FLOAT,
    start_date TIMESTAMP WITHOUT TIME ZONE,
    end_date TIMESTAMP WITHOUT TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    title_ua VARCHAR(128),
    title_en VARCHAR(128),
    title_de VARCHAR(128),
    title_ru VARCHAR(128),
    description_ua TEXT,
    description_en TEXT,
    description_de TEXT,
    description_ru TEXT
);

-- Token Purchases
CREATE TABLE IF NOT EXISTS token_purchase (
    id SERIAL PRIMARY KEY,
    token_sale_id INTEGER REFERENCES token_sale(id),
    user_id INTEGER REFERENCES "user"(id),
    wallet_address VARCHAR(42),
    amount FLOAT,
    price FLOAT,
    total_paid FLOAT,
    payment_method_id INTEGER REFERENCES payment_method(id),
    status VARCHAR(32) DEFAULT 'pending',
    tx_hash VARCHAR(66),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- DAO Proposals
CREATE TABLE IF NOT EXISTS dao_proposal (
    id SERIAL PRIMARY KEY,
    title VARCHAR(128),
    description TEXT,
    author_id INTEGER REFERENCES "user"(id),
    start_date TIMESTAMP WITHOUT TIME ZONE,
    end_date TIMESTAMP WITHOUT TIME ZONE,
    min_tokens_to_vote FLOAT DEFAULT 1.0,
    status VARCHAR(32) DEFAULT 'pending',
    votes_for INTEGER DEFAULT 0,
    votes_against INTEGER DEFAULT 0,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    title_ua VARCHAR(128),
    title_en VARCHAR(128),
    title_de VARCHAR(128),
    title_ru VARCHAR(128),
    description_ua TEXT,
    description_en TEXT,
    description_de TEXT,
    description_ru TEXT
);

-- DAO Votes
CREATE TABLE IF NOT EXISTS dao_vote (
    id SERIAL PRIMARY KEY,
    proposal_id INTEGER REFERENCES dao_proposal(id),
    user_id INTEGER REFERENCES "user"(id),
    wallet_address VARCHAR(42),
    vote_weight FLOAT,
    vote_for BOOLEAN,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    tx_hash VARCHAR(66)
);

-- Blog Blocks
CREATE TABLE IF NOT EXISTS blog_block (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    featured_image VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    position INTEGER DEFAULT 1,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
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

-- Image Storage
CREATE TABLE IF NOT EXISTS image_storage (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) UNIQUE NOT NULL,
    binary_data BYTEA,
    content_type VARCHAR(128),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- Blog Topics (from blog_automation models)
CREATE TABLE IF NOT EXISTS blog_topic (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    scheduled_for TIMESTAMP WITHOUT TIME ZONE,
    blog_block_id INTEGER REFERENCES blog_block(id)
);

-- Autoposting Schedule (from blog_automation models)
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
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- Content Generation Logs (from blog_automation models)
CREATE TABLE IF NOT EXISTS content_generation_log (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES blog_topic(id) ON DELETE SET NULL,
    action VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'success',
    message TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    duration_seconds FLOAT
);

-- Create extension for UUID support if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
