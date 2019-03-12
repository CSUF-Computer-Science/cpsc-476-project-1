--
-- File generated with SQLiteStudio v3.2.1 on Mon Mar 4 15:43:18 2019
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = on;
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS users;

-- Table: articles
CREATE TABLE articles (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT (128), content TEXT (512), author INT REFERENCES users (username), posted datetime DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')));

-- Table: comments
CREATE TABLE comments (id INTEGER PRIMARY KEY AUTOINCREMENT, author STRING (32) REFERENCES users (username), content TEXT, article INT REFERENCES articles (id), posted datetime DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')));

-- Table: tags
CREATE TABLE tags (name STRING (16), article INT REFERENCES articles(id), UNIQUE (name, article) ON CONFLICT FAIL);

-- Table: users
CREATE TABLE users (username STRING (32) PRIMARY KEY ON CONFLICT FAIL, password TEXT, full_name STRING (64));

-- Create entry for anonymous users, required for foreign keys
INSERT INTO users (username, password, full_name) VALUES ("Anonymous Coward", "invalidhash", "Anonymous Coward");
                                                                                                        
