import mysql.connector
obj=mysql.connector.connect(host="localhost",database="AZTURA",user="root",password="rishmi@123")
c=obj.cursor()

for i in range(4):
    c.execute("use AZTURA")
    c.execute("insert into score_card values(%s,100)")
    c.execute("select * from score_card")
    l=c.fetchall() #l=list of tuples
    print(l)
c.close()
obj.close()
