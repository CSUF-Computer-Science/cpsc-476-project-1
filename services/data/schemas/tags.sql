DROP TABLE IF EXISTS tags;
CREATE TABLE tags (name STRING (16), article INT, UNIQUE (name, article) ON CONFLICT FAIL);
