CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    headline VARCHAR(500) NOT NULL,
    source VARCHAR(200) NOT NULL DEFAULT 'Unknown',
    url VARCHAR(1000) NOT NULL UNIQUE,
    sentiment VARCHAR(20) NOT NULL,
    topic VARCHAR(50) NOT NULL,
    published_date DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_articles_headline_source UNIQUE (headline, source)
);

CREATE INDEX IF NOT EXISTS ix_articles_brand ON articles (brand);
CREATE INDEX IF NOT EXISTS ix_articles_sentiment ON articles (sentiment);
CREATE INDEX IF NOT EXISTS ix_articles_topic ON articles (topic);
CREATE INDEX IF NOT EXISTS ix_articles_published_date ON articles (published_date);

CREATE TABLE IF NOT EXISTS daily_sentiment (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    articles INTEGER NOT NULL DEFAULT 0,
    positive INTEGER NOT NULL DEFAULT 0,
    neutral INTEGER NOT NULL DEFAULT 0,
    negative INTEGER NOT NULL DEFAULT 0,
    score DOUBLE PRECISION NOT NULL DEFAULT 0,
    CONSTRAINT uq_daily_sentiment_brand_date UNIQUE (brand, date)
);

CREATE INDEX IF NOT EXISTS ix_daily_sentiment_brand ON daily_sentiment (brand);
CREATE INDEX IF NOT EXISTS ix_daily_sentiment_date ON daily_sentiment (date);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    id SERIAL PRIMARY KEY,
    status VARCHAR(30) NOT NULL DEFAULT 'running',
    total_fetched INTEGER NOT NULL DEFAULT 0,
    total_processed INTEGER NOT NULL DEFAULT 0,
    total_added INTEGER NOT NULL DEFAULT 0,
    error_message TEXT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ NULL
);

CREATE INDEX IF NOT EXISTS ix_pipeline_runs_status ON pipeline_runs (status);

CREATE TABLE IF NOT EXISTS pipeline_brand_progress (
    id SERIAL PRIMARY KEY,
    run_id INTEGER NOT NULL REFERENCES pipeline_runs(id) ON DELETE CASCADE,
    brand VARCHAR(50) NOT NULL,
    fetched INTEGER NOT NULL DEFAULT 0,
    processed INTEGER NOT NULL DEFAULT 0,
    added INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_pipeline_brand_progress_run_brand UNIQUE (run_id, brand)
);

CREATE INDEX IF NOT EXISTS ix_pipeline_brand_progress_run_id ON pipeline_brand_progress (run_id);
CREATE INDEX IF NOT EXISTS ix_pipeline_brand_progress_brand ON pipeline_brand_progress (brand);
