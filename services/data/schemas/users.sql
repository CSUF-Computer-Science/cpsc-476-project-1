DROP TABLE IF EXISTS users;
CREATE TABLE users (username STRING (32) PRIMARY KEY ON CONFLICT FAIL, password TEXT, full_name STRING (64));

