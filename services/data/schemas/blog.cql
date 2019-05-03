CREATE KEYSPACE IF NOT EXISTS blog WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};
USE blog;
CREATE TABLE IF NOT EXISTS articles (id timeuuid PRIMARY KEY, title text, content text, author text, posted timestamp);
CREATE TABLE IF NOT EXISTS comments (id timeuuid PRIMARY KEY, author text, content text, article timeuuid, posted timestamp);
CREATE INDEX IF NOT EXISTS comments_article ON comments (article);
CREATE TABLE IF NOT EXISTS tags (name text, article int, PRIMARY KEY(name, article));
CREATE TABLE IF NOT EXISTS users (username text PRIMARY KEY, password text, full_name text);