import sqlite3


#Here we will make database file to store some data from our dataframe
connection = sqlite3.connect("customers.db")
cursor = connection.cursor()
