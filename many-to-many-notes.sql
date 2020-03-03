-- many to many relationship

-- STEP 1 CREATING A TABLE/STORAGE FOR DATABASE
CREATE TABLE User (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	name TEXT,
	email TEXT
);

CREATE TABLE Course (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	title Text
);


-- CONNECTOR TABLE FOR MANY TO MANY RELATIONSHIP
CREATE TABLE Member (
	user_id INTEGER,
	course_id INTEGER,
	role INTEGER,

	-- primary key for MANY TO MANY is actually 2 columns of foreign key
	PRIMARY KEY (user_id, course_id)
)


-- STEP 2 INSERTING VALUES INSIDE TABLE/STORAGE
INSERT INTO User (name,email) VALUES ('Jane', 'jane@tsugi.org');
INSERT INTO User (name,email) VALUES ('Ed', 'ed@tsugi.org');
INSERT INTO User (name,email) VALUES ('Sue', 'sue@tsugi.org');
INSERT INTO Course (title) VALUES ('Python');
INSERT INTO Course (title) VALUES ('SQL');
INSERT INTO Course (title) VALUES ('PHP');

-- STEP 3 INSERTING VALUES INTO JUNCTION TABLE
INSERT INTO Member (user_id,course_id,role) VALUES (1,1,1);
INSERT INTO Member (user_id,course_id,role) VALUES (2,1,0);
INSERT INTO Member (user_id,course_id,role) VALUES (3,1,0);

INSERT INTO Member (user_id,course_id,role) VALUES (1,2,0);
INSERT INTO Member (user_id,course_id,role) VALUES (2,2,1);

INSERT INTO Member (user_id,course_id,role) VALUES (2,3,1);
INSERT INTO Member (user_id,course_id,role) VALUES (3,3,0);

-- STEP 4 SELECT FROM JOINED TABLE ON A FILTER WITH ORDER
SELECT User.name, Member.role, Course.title
FROM User JOIN Member JOIN Course
ON Member.user_id = User.id AND Member.course_id = Course.id
-- ORDER BY PRECEDENCE, 1ST PRIORITY, 2ND PRIORITY, 3RD PRIORITY..
ORDER BY Course.title, Member.role DESC, User.name