import psycopg2
con = psycopg2.connect(
	host = "127.0.0.1",
	dbname = "postgres",
	user = "postgres",
	password = "postgres"
	)
cursor = con.cursor()
# cursor.execute("INSERT into conferences (id, date, location, title) values (%s, %s, %s ,%s)",(1,"asd","dsa","sss"))
cursor.execute("DELETE from conferences WHERE id<>0")
con.commit()
cursor.close()
con.close()