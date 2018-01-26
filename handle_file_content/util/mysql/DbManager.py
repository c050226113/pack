import pymysql


class DbManager:
    @staticmethod
    def create_db(host, user, password, port=3306, charset='utf8', ):
        return pymysql.connect(
            host=host, user=user, passwd=password, port=port, charset=charset
        )
