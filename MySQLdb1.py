import MySQLdb  
db = MySQLdb.connect("localhost","petstore","oyj7766","petstore" )  
cursor = db.cursor()  
cursor.execute("SELECT VERSION()")  
data = cursor.fetchone()      
print "Database version : %s " % data      
db.close()
