# app/models.py
# 用于存储数据库实例信息
# 注意：不存业务数据，只存管理信息
class DBInstance:
    def __init__(self, name, db_type, host, port, user, password):
        self.name = name
        self.db_type = db_type  # mysql/postgresql
        self.host = host
        self.port = port
        self.user = user
        self.password = password

# 示例数据
instances = [
    DBInstance('Test MySQL', 'mysql', 'localhost', 3306, 'root', 'test0120')
]