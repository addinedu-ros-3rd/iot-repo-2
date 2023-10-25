import mysql.connector
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')
dev = config['dev']

remote = mysql.connector.connect(
	user = dev['user'],
    password = dev['password'],
    port = dev['port'],
	host = dev['host'],
	database = dev['database'])

cursor = remote.cursor()

query = "select category_id from rfid"
cursor.execute(query)
category_id = cursor.fetchone()[0]

print(category_id)
            