BEGIN TRANSACTION;
CREATE TABLE association (
	book_id INTEGER, 
	writer_id INTEGER, 
	FOREIGN KEY(book_id) REFERENCES books (id), 
	FOREIGN KEY(writer_id) REFERENCES writers (id)
);
INSERT INTO association VALUES(3,2);
INSERT INTO association VALUES(4,3);
INSERT INTO association VALUES(5,4);
INSERT INTO association VALUES(6,3);
INSERT INTO association VALUES(6,5);
INSERT INTO association VALUES(2,2);
INSERT INTO association VALUES(7,1);
CREATE TABLE books (
	id INTEGER NOT NULL, 
	title VARCHAR, 
	PRIMARY KEY (id)
);
INSERT INTO books VALUES(2,1984);
INSERT INTO books VALUES(3,'Animal Farm: A Fairy Story');
INSERT INTO books VALUES(4,'The Lord of the Rings');
INSERT INTO books VALUES(6,'Hobbit');
INSERT INTO books VALUES(7,'One Flew Over the Cuckoo’s Nest');
CREATE TABLE users (
	id INTEGER NOT NULL, 
	email VARCHAR NOT NULL, 
	password VARCHAR NOT NULL, 
	first_name VARCHAR, 
	last_name VARCHAR, 
	staff BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (email), 
	CHECK (staff IN (0, 1))
);
INSERT INTO users VALUES(1,'admin@admin.com','admin','admin','admin',1);
CREATE TABLE writers (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	PRIMARY KEY (id)
);
INSERT INTO writers VALUES(1,'Ken Elton Kesey');
INSERT INTO writers VALUES(2,'George Orwell');
INSERT INTO writers VALUES(3,'John Ronald Reuel Tolkien');
INSERT INTO writers VALUES(4,'William Gerald Golding');
COMMIT;
