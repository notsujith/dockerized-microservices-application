DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
    first_name TEXT, 
    last_name TEXT,
    username TEXT UNIQUE, 
    email_address TEXT,
    hashed_pass TEXT,  
    salt TEXT,
    groups TEXT,
    PRIMARY KEY (username, email_address)
);

DROP TABLE IF EXISTS passwords;
CREATE TABLE IF NOT EXISTS passwords(
    user_name TEXT PRIMARY KEY,
    previous_hashed_pass TEXT,
    FOREIGN KEY (user_name) REFERENCES users(username)
        ON DELETE CASCADE ON UPDATE CASCADE
);
