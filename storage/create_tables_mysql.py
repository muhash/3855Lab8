import mysql.connector

db_conn = mysql.connector.connect(host="sba.eastus.cloudapp.azure.com", user="tamik", password="password", database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
          CREATE TABLE ordr
          (id INT NOT NULL AUTO_INCREMENT, 
           customer_id VARCHAR(250) NOT NULL,
           ordr VARCHAR(250) NOT NULL,
           price INT NOT NULL,
           address VARCHAR(250) NOT NULL,
           timestamp VARCHAR(250) NOT NULL,
           date_created VARCHAR(250) NOT NULL,
           CONSTRAINT ordr_pk PRIMARY KEY (id))
          ''')

db_cursor.execute('''
          CREATE TABLE destination
          (id INT NOT NULL AUTO_INCREMENT,
           home_address VARCHAR(250) NOT NULL,
           dest_address VARCHAR(250) NOT NULL,
           num_passengers INTEGER NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT destination_pk PRIMARY KEY (id))
          ''')

db_conn.commit()
db_conn.close()
