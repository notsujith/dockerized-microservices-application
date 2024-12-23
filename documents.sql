DROP TABLE IF EXISTS documents;
CREATE TABLE IF NOT EXISTS documents(
    filename TEXT PRIMARY KEY,
    groups TEXT,
    owner TEXT,
    last_mod TEXT,
    file_hash TEXT,
    total_mods INTEGER DEFAULT 1
);
