CREATE_CLIENT_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS users(
        user_id SERIAL PRIMARY KEY,
        username TEXT DEFAULT NULL,
        name CHARACTER VARYING DEFAULT NULL,
        surname CHARACTER VARYING DEFAULT NULL,
        time TIMESTAMP,
        current_char_id INT DEFAULT 1,
        FOREIGN KEY (current_char_id) REFERENCES characters(char_id)
    );"""

CREATE_CHAR_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS characters(
        char_id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        welcome_msg TEXT NOT NULL
    );"""

CREATE_PROMTS_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS promts(
        promt_id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        character_id INT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (character_id) REFERENCES characters(char_id)
    );"""
