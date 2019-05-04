CREATE KEYSPACE IF NOT EXISTS blog WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};
USE blog;
CREATE TABLE IF NOT EXISTS articles (id timeuuid, author text, title text, content text, posted timestamp, PRIMARY KEY(id));
CREATE INDEX article_author ON articles(author);
CREATE TABLE IF NOT EXISTS comments (id timeuuid, author text, content text, article timeuuid, posted timestamp, PRIMARY KEY(article, id, author));
CREATE TABLE IF NOT EXISTS tags (name text, article uuid, PRIMARY KEY(article, name));
CREATE TABLE IF NOT EXISTS users (username text PRIMARY KEY, password text, full_name text);