# Instructions
# This application will read roster data in JSON format, parse the file, and then produce an SQLite database that contains a User, Course, and Member table and populate the tables from the data file.
# 
# You can base your solution on this code: http://www.py4e.com/code3/roster/roster.py - this code is incomplete as you need to modify the program to store the role column in the Member table to complete the assignment.
# 
# Each student gets their own file for the assignment. Download this file and save it as roster_data.json. Move the downloaded file into the same folder as your roster.py program.
# 
# Once you have made the necessary changes to the program and it has been run successfully reading the above JSON data, run the following SQL command:
# 
# SELECT hex(User.name || Course.title || Member.role ) AS X FROM 
#     User JOIN Member JOIN Course 
#     ON User.id = Member.user_id AND Member.course_id = Course.id
#     ORDER BY X
# Find the first row in the resulting record set and enter the long string that looks like 53656C696E613333.



# import library json and sqlite3
import json
import sqlite3

# create a connection object that represents the database
conn = sqlite3.connect('rosterdb.sqlite')

# create a file handler for database
cur = conn.cursor()

# Execute multiple script
# wipe out data if exist
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Member;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

# file handler XML OR JSON
fname = input('Enter file name: ')

# if length of input is < 1 meaning if the user just entered and did not type anything on the input
if len(fname) < 1:

    # ..the default value of fname will be roster_data_sample.json
    fname = 'roster_data.json'

# [
#   [ "Charley", "si110", 1 ],
#   [ "Mea", "si110", 0 ],

str_data_before = open(fname)
print("the data type of str_data is" + str(type(str_data_before)))
print(str_data_before)

str_data_after = str_data_before.read()
print("the data type of str_data is" + str(type(str_data_after)))
print(str_data_after)

json_data = json.loads(str_data_after)
print("the data type of json_data is" + str(type(json_data)))
print(json_data)

print("Looping for each entry in json_data...")
# INSERTING THE DATA
for entry in json_data:

    user = entry[0];
    course = entry[1];
    instructor = entry[2]

    print("Executing SQL statements")

    # insert or ignore means if it blows up, just ignore it,
    # OR IGNORE MEANS MAKE SURE THE INSERTED IS ALREADY IN TABLE AND
    # NO DUPLICATES ARE INSERTED

    # INSERTING USER
    sql_statement = '''
    INSERT OR IGNORE INTO User (name)
    VALUES (?)
    '''
    sql_value = (user, )
    cur.execute(sql_statement, sql_value)

    # INSERTING COURSE
    sql_statement = '''
    INSERT OR IGNORE INTO Course (title)
    VALUES (?)
    '''
    sql_value = (course,)
    cur.execute(sql_statement,sql_value)

    # GETTING USER
    sql_statement = '''
    SELECT id FROM User
    WHERE name = (?)
    '''
    sql_value = (user,)
    cur.execute(sql_statement, sql_value)
    userid = cur.fetchone()[0]
    print(userid)

    # GETTING COURSE
    sql_statement = '''
    SELECT id FROM Course
    WHERE title = (?)
    '''
    sql_value = (course,)
    cur.execute(sql_statement,sql_value)
    courseid = cur.fetchone()[0]
    print(courseid)

    # INSERTING ENTRY TO JUNCTION
    sql_statement = '''
    INSERT OR REPLACE INTO Member (user_id, course_id, role)
    VALUES (?,?,?)
    '''
    sql_value = (userid, courseid, instructor)
    cur.execute(sql_statement, sql_value)


print("Commiting..")
print("Saving changes..")
conn.commit()
print("Commiting done!")


# TESTING AND OBTAINING RESULT
test_statement = '''
SELECT hex(User.name || Course.title || Member.role)
AS X
FROM User JOIN Member JOIN Course
ON User.id = Member.user_id AND Member.course_id = Course.id
ORDER BY X
'''
cur.execute(test_statement)
result = cur.fetchone()
print("RESULT: " + str(result))

# Closing the connection
cur.close()
conn.close()