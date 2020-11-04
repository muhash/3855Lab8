import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE ordr
          (id INTEGER PRIMARY KEY ASC, 
           customer_id VARCHAR(250) NOT NULL,
           ordr VARCHAR(250) NOT NULL,
           price INTEGER NOT NULL,
           address VARCHAR(250) NOT NULL,
           timestamp VARCHAR(250) NOT NULL,
           date_created VARCHAR(250) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE destination
          (id INTEGER PRIMARY KEY ASC, 
           home_address VARCHAR(250) NOT NULL,
           dest_address VARCHAR(250) NOT NULL,
           num_passengers INTEGER NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
