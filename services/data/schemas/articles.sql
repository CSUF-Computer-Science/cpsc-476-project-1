DROP TABLE IF EXISTS articles;
CREATE TABLE articles (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT (128), content TEXT (512), author INT, posted datetime DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')));
