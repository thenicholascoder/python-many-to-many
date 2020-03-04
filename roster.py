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
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

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
    fname = 'roster_data_sample.json'

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

    name = entry[0];
    title = entry[1];

    print((name, title))

    print("Executing SQL statements")

    # insert or ignore means if it blows up, just ignore it,
    # OR IGNORE MEANS MAKE SURE THE INSERTED IS ALREADY IN TABLE AND
    # NO DUPLICATES ARE INSERTED
    sql_statement = '''
    INSERT OR IGNORE INTO User (name)
    VALUES ?
    '''
    sql_value = name
    cur.execute(sql_statement, sql_value)





    # get the id
    sql_statement = '''
    SELECT id FROM User
    WHERE name = ?
    '''
    sql_value = name
    cur.execute(sql_statement, sql_value)
    user_id = cur.fetchone()[0]






    sql_statement = '''
    INSERT OR IGNORE INTO Course (title)
    VALUES ?
    '''
    sql_value = title
    cur.execute(sql_statement, sql_value)



    sql_statement = '''
    SELECT id FROM Course
    WHERE title = ?
    '''
    sql_value = title
    cur.execute(sql_statement, sql_value)
    course_id = cur.fetchone()[0]


    # if there is a duplicate, if combinication is already there then theis will be automatically become update request
    sql_statement = '''
    INSERT OR REPLACE INTO Member (user_id, course_id)
    VALUES (?,?)
    '''
    sql_value = (user_id,course_id)
    cur.execute(sql_statement, sql_value)


print("Commiting..")
conn.commit()
print("Commiting done!")
