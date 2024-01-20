# SQLite 管理类
import sqlite3
from typing import List, Tuple
from utils.path import PathManager as pm


# 单例模式
class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self, *args, **kwargs):
        # if self._cls not in self._instance:
        #     self._instance[self._cls] = self._cls()
        # return self._instance[self._cls]
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls(*args, **kwargs)
        return self._instance[self._cls]

    # q: 当这个类当作装饰器使用时，运行逻辑是怎么样的
    # a: 1. 例如：@Singleton class SqliteManager: ...
    #    2. 在新建一个 SqliteManager 的实例时，会先把 SqliteManager 传入 Singleton 的 __init__ 方法
    #    3. 然后调用 __call__ 方法，返回一个 SqliteManager 的实例
    #    4. 之后再新建 SqliteManager 的实例时，就会直接返回之前创建的实例
    #    5. 这样就保证了 SqliteManager 的实例只有一个


@Singleton
class SqliteManager:
    """SQLite 管理类"""

    def __init__(self, db_file_path: str) -> None:
        """初始化"""
        self.db_file_path = pm.get_abs_path(db_file_path)
        self.conn = sqlite3.connect(self.db_file_path)
        self.cursor = self.conn.cursor()

    def __del__(self) -> None:
        """析构"""
        self.cursor.close()
        self.conn.close()

    def execute(self, sql: str, params: Tuple = ()) -> None:
        """执行 SQL 语句
        :param sql: SQL 语句
        :param params: 可选参数（元组）
        """
        self.cursor.execute(sql, params)
        self.conn.commit()

    def fetch_all(self, sql: str, params: Tuple = ()) -> List:
        """查询所有
        :param sql: SQL 语句
        :param params: 可选参数（元组）
        """
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def fetch_one(self, sql: str, params: Tuple = ()) -> Tuple:
        """查询一条
        :param sql: SQL 语句
        :param params: 可选参数（元组）
        """
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def insert(self, table: str, data: dict) -> None:
        """插入数据
        :param table: 表名
        :param data: 插入的数据，字典类型，key 为字段名，value 为字段值
        """
        keys = ", ".join(data.keys())
        values = ", ".join(["?"] * len(data))
        sql = f"INSERT INTO {table}({keys}) VALUES({values})"
        self.cursor.execute(sql, tuple(data.values()))
        self.conn.commit()

    def update(self, table: str, data: dict, condition: str) -> None:
        """更新数据
        :param table: 表名
        :param data: 更新的数据，字典类型，key 为字段名，value 为字段值
        :param condition: 更新条件
        """
        keys = ", ".join([f"{key} = ?" for key in data.keys()])
        sql = f"UPDATE {table} SET {keys} WHERE {condition}"
        self.cursor.execute(sql, tuple(data.values()))
        self.conn.commit()

    def delete(self, table: str, condition: str) -> None:
        """删除数据
        :param table: 表名
        :param condition: 删除条件
        """
        sql = f"DELETE FROM {table} WHERE {condition}"
        self.cursor.execute(sql)
        self.conn.commit()

    def create_table(self, table: str, columns: List) -> None:
        """创建表
        :param table: 表名
        :param columns: 字段列表，列表元素为字段名和字段类型，例如：["id INTEGER PRIMARY KEY", "name TEXT"]
        """
        columns_str = ", ".join(columns)
        sql = f"CREATE TABLE {table}({columns_str})"
        self.cursor.execute(sql)
        self.conn.commit()

    def check_and_create_table(self, table: str, columns: List) -> None:
        """检查并创建表
        :param table: 表名
        :param columns: 字段列表，列表元素为字段名和字段类型，例如：["id INTEGER PRIMARY KEY", "name TEXT"]
        """
        sql = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"
        result = self.fetch_one(sql)
        if result is None:
            self.create_table(table, columns)
