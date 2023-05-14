import pymysql

from common.LogHandle import Logger


class mysql:
    def __init__(self):
        self._host = 'localhost'
        self._port = 3306
        self._user = 'root'
        self._password = '123456'
        self._database = 'api_db'
        self.log = Logger("mysql")
        try:
            self.mysql_connect = pymysql.connect(host=self._host, port=self._port, user=self._user,
                                                 password=self._password,
                                                 database=self._database)
        except Exception as e:
            self.log.error(f"数据库连接失败！erroe：{e}")
        self.mysql_cursor = self.mysql_connect.cursor()

    def search_execute(self, args, num: int = None):
        self.mysql_cursor.execute(args)
        if num is not None:
            result = self.mysql_cursor.fetchmany(num)
            print(f"更新结果：{result}")
        else:
            result = self.mysql_cursor.fetchall()
            print(f"更新结果：{result}")
        return bool(result)

    def update_execute(self, args):
        result = self.mysql_cursor.execute(args)
        return result

    def insert_execute(self, args):
        result = self.mysql_cursor.execute(args)
        print(f"insert插入结果：{result}")
        return result

    def del_execute(self, args):
        result = self.mysql_cursor.execute(args)
        print(f"del删除结果：{result}")
        return result

    def close(self):
        self.mysql_cursor.close()
        self.mysql_connect.close()
        print("sql断开连接成功")


if __name__ == '__main__':
    sql = mysql()

    # 查询全部
    sql.search_execute("select * from sp_manager")

    # 查询2条
    sql.search_execute("select * from sp_manager", 2)

    # 更新数据
    sql.update_execute("UPDATE sp_manager SET mg_mobile=3333 WHERE mg_id=516")

    # 插入数据
    sql.insert_execute(
        "insert into sp_manager(mg_name,mg_pwd,mg_time) VALUES('hpj23','$10$ZI8rwedLU7ROHiLBC2t4uuzebY6rooLQZ9KN2gAgIoURg5plo.1yy','1683651315')")

    # 删除数据
    sql.del_execute("delete from sp_manager where mg_id=515")

    # 关闭数据库
    sql.close()
