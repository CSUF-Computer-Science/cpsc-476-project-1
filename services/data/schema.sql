--
-- File generated with SQLiteStudio v3.2.1 on Mon Mar 4 15:43:18 2019
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS users;

-- Table: articles
CREATE TABLE articles (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT (128), content TEXT (512), author INT REFERENCES users (username), posted datetime default CURRENT_TIMESTAMP);
INSERT INTO articles (title, content, author) VALUES ("My Fake Twitter BIO", "I'm a cat fan", "testuser");
-- Table: comments
CREATE TABLE comments (id INTEGER PRIMARY KEY AUTOINCREMENT, author INT REFERENCES users (username), content TEXT, article INT REFERENCES articles (id), posted datetime default CURRENT_TIMESTAMP);
INSERT INTO comments (author, article, content) VALUES ("testuser", 1, "that's super cool");

-- Table: tags
CREATE TABLE tags (name STRING (16), article INT REFERENCES articles, UNIQUE (name, article) ON CONFLICT FAIL);
INSERT INTO tags (article, name) VALUES (1, "blessed");
INSERT INTO tags (article, name) VALUES (1, "stayblessed");
-- Table: users
CREATE TABLE users (username STRING (32) PRIMARY KEY ON CONFLICT FAIL, password TEXT, full_name STRING (64));
-- INSERT INTO users (username, password, full_name) VALUES ("testuser", "$2b$12$DbmIZ/a5LByoJHgFItyZCeyg/DVecJAzVzmtVfFGKioGo8AqWE1XC", "Test User");

PRAGMA foreign_keys = on;