import pymysql


class Connection:
    def __init__(self, host, user, password, db, port=3306, charset='utf8'):
        self.conn = pymysql.connect(
            host=host, user=user, passwd=password, port=port, charset=charset
        )
        self.dbName = db
        self.conn.select_db(self.dbName)

    def close(self):
        self.conn.close()

    def cursor(self):
        return self.conn.cursor()
