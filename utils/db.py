import pymysql
from mate_config import config


class Database:
    def __init__(self):
        host = "remotemysql.com"
        user = "2OPrqL0Qb3"
        passwd = config.get("mysql_password")
        database = "2OPrqL0Qb3"
        self.con = pymysql.connect(host=host, user=user, passwd=passwd, \
                                   db=database, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def create_table(self):
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS requests(
                     id INT auto_increment,
                    user_name varchar(255) NOT NULL ,
                    content TEXT,
                    PRIMARY KEY (id)
                );
                """)

    def make_request(self, user_name, content):
        sql_query = "INSERT INTO requests (user_name, content) VALUES (%s, %s);"
        self.cur.execute(sql_query, (user_name, content))
        self.con.commit()

    def get_requests(self):
        sql_query = "SELECT * FROM requests"
        self.cur.execute(sql_query)
        return self.cur.fetchall()

    def __del__(self):
        self.cur.close()
        self.con.close()