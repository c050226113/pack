from util.lib.TYPE import TYPE
from util.lib.Util import Util


class MysqlTable:
    def __init__(self, conn, table_name):
        self.table_name = '`' + table_name + '`'
        self.table_cursor = conn.cursor()
        self.conn = conn

    @staticmethod
    def make_select(select_list):
        if not TYPE.is_list(select_list):
            return '*'
        new_list = []
        for item in select_list:
            new_list.append('`' + item + '`')
        return ','.join(new_list)

    @staticmethod
    def make_where_item(item):
        if not TYPE.is_list(item):
            item = [item, '=', 'and']
        else:
            length = len(item)
            if length < 2:
                item.append('=')
                item.append('and')
            elif length < 3:
                item.append('and')
        if TYPE.is_str(item[0]):
            item[0] = "'" + Util.addslashes(item[0]) + "' " + item[2] + " "
        elif TYPE.is_int(item[0]):
            item[0] = str(item[0]) + " " + item[2] + " "
        return item

    def make_where(self, where_dict):
        if not TYPE.is_dict(where_dict):
            return '1=1'
        where_str = ''
        for key in where_dict:
            val = where_dict[key]
            if TYPE.is_tuple(val):
                for item in val:
                    item = self.make_where_item(item)
                    where_str += "`" + key + "`" + item[1] + item[0]
            else:
                item = self.make_where_item(val)
                where_str += "`" + key + "`" + str(item[1]) + str(item[0])
        return where_str[:-4]

    @staticmethod
    def make_set(set_dict):
        set_str = ''
        for key in set_dict:
            val = set_dict[key]
            if TYPE.is_str(val):
                val = "'" + Util.addslashes(val) + "',"
            elif TYPE.is_int(val):
                val = str(val) + ','
            set_str += "`" + key + "`=" + val
        return set_str[:-1]

    def find_one(self, select_list=None, where_dict=None):
        select_str = self.make_select(select_list)
        where_str = self.make_where(where_dict)
        sql = "SELECT " + select_str + " FROM " + self.table_name + " WHERE " + where_str
        return self.get_obj_by_sql(sql)

    def find_all(self, select_list=None, where_dict=None):
        select_str = self.make_select(select_list)
        where_str = self.make_where(where_dict)
        sql = "SELECT " + select_str + " FROM " + self.table_name + " WHERE " + where_str
        return self.get_obj_arr_by_sql(sql)

    def update_one(self, set_dict=None, where_dict=None):
        if not where_dict or not set_dict:
            return False
        where_str = self.make_where(where_dict)
        set_str = self.make_set(set_dict)
        sql = "UPDATE " + self.table_name + " SET " + set_str + " WHERE " + where_str
        return self.operator_obj_by_sql(sql)

    def add_one(self, set_dict=None):
        if not set_dict:
            return False
        set_str = self.make_set(set_dict)
        sql = "INSERT INTO " + self.table_name + " SET " + set_str
        res = self.operator_obj_by_sql(sql)
        if not res:
            print(set_dict)
            print(sql)
        return res

    def operator_obj_by_sql(self, sql):
        try:
            if self.table_cursor.execute(sql):
                return True
            else:
                return False
        except:
            Util.err()
            return False

    def get_obj_by_sql(self, sql):
        try:
            self.table_cursor.execute(sql)
            row = self.table_cursor.fetchone()
            if TYPE.is_tuple(row):
                return row
            else:
                return False
        except:
            Util.err(sql)
            return False

    def get_obj_arr_by_sql(self, sql):
        self.table_cursor.execute(sql)
        rows = self.table_cursor.fetchall()
        if TYPE.is_tuple(rows):
            return rows
        else:
            return False

    def close(self):
        self.table_cursor.close()
