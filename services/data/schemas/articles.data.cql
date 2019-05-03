INSERT INTO articles (title, content, author) VALUES ('My Article Should Never Appear On Latest', 'Because I posted too early', 'testuser');
INSERT INTO articles (title, content, author) VALUES ("My Original Fake Twitter BIO", "I'm a cat fan", "testuser");
INSERT INTO articles (title, content, author) VALUES ("My Fake Twitter BIO 1", "I'm a bird fan", "testuser");
INSERT INTO articles (title, content, author) VALUES ("My Fake Twitter BIO 2", "I'm a turtle fan", "testuser");
INSERT INTO articles (title, content, author) VALUES ("My Fake Twitter BIO 3", "I'm a dog fan", "testuser");
INSERT INTO articles (title, content, author) VALUES ("My Fake Twitter BIO 4", "I'm a rabbit fan", "testuser");
INSERT INTO articles (title, content, author) VALUES ("Information is plentiful but harder to digest", "In reality, this translates into a lot of book orders, blog searches, and Twitter scans.
While more information is becoming available on the Internet and more and more books are being published, even on topics that are relatively new, one aspect that continues to inhibit us is the inability to find concise technology overview books.", "markosvaljek");
INSERT INTO articles (title, content, author) VALUES ("Data Update, Removal, and Compaction", "Cassandra does not do any insert or update operations on written data. This would require random I/O operations, which are not very efficient. If data is updated or inserted, Cassandra simply writes new data with a new timestamp into the memtable and then into the SSTable. As time progresses, the redundant data accumulates; this redundant data is then removed in a process called compaction.
", "markosvaljek");
INSERT INTO articles (title, content, author) VALUES ("CQL", "CQL, or Cassandra Query Language, is not the only way of interacting with Cassandra. Not long ago, Thrift API was the main way of interacting with it. The usage, organization, and syntax of this API were oriented toward exposing the internal mechanisms of Cassandra storage directly to the user.", "markosvaljek");
INSERT INTO articles (title, content, author) VALUES ("Cluster Ordering the Data", "Tip: Clustering sorts the data within the partition, not the partitions.", "markosvaljek");
INSERT INTO articles (title, content, author) VALUES ("Cassandra Strings", "Strings are always placed inside single quotation marks. If you need the single quotation mark in the data, escape it with another single quotation mark before placing it in the string ", "markosvaljek");


