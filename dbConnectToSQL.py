import mysql.connector

class DbConnectSQL:
    def __init__(self) -> None:
        with open("config.txt") as f:
            rawdata = [line.rstrip() for line in f]
        self.mydb = mysql.connector.connect(
            host=rawdata[0],
            user=rawdata[1],
            password=rawdata[2],
            database=rawdata[3]
        )
        self.mycursor = self.mydb.cursor()
        # self.mycursor.execute("SHOW DATABASES")
        # for x in self.mycursor:
        #     print(x)