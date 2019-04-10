DROP TABLE IF EXISTS comments;
CREATE TABLE comments (id INTEGER PRIMARY KEY AUTOINCREMENT, author STRING (32), content TEXT, article INT, posted datetime DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')));
