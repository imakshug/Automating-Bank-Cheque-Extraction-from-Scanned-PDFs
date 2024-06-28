import mysql.connector

conn=mysql.connector.connect(host='localhost', username='root',password='mysql10', database='pdf_to_img')
cursor=conn.cursor()

conn.commit()
conn.close()

print("Connect succefully created!")