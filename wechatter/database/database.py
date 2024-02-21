from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wechatter.database.tables import Base
from wechatter.utils.path_manager import get_abs_path

DB_PATH = get_abs_path("data/wechatter.sqlite")

engine = create_engine(f"sqlite:///{DB_PATH}")


# 创建数据库会话函数，在上下文管理器中使用
make_db_session = sessionmaker(engine)


# 创建数据库表
def create_tables():
    Base.metadata.create_all(engine, checkfirst=True)
