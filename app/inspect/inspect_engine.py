import yaml
import os


def get_db_version(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("select version()")
        version = cursor.fetchone()[0].lower()
        return  version
    finally:
        cursor.close()

def version_matches(item_version, db_version):
    """
    判断 YAML 中的版本 item_version 是否匹配数据库版本 db_version
    支持主+次版本匹配，例如 5.6, 5.7, 8.0
    """
    if not item_version:
        return True  # 没指定版本，默认匹配

    # 提取数据库主+次版本
    parts = db_version.split(".")
    if len(parts) < 2:
        return False
    major_minor = f"{parts[0]}.{parts[1]}"

    return str(item_version) == major_minor

def load_inspect_sql(inspect_type, db_name, table_name,  db_version=None):

    base_dir = os.path.dirname(__file__)
    yaml_file = os.path.join(base_dir, "inspect_sql.yaml")

    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    sql_list = []

    if inspect_type in data:
        for item in data[inspect_type]:


            # 版本过滤
            if db_version and item.get("version"):
                if not version_matches(item["version"], db_version):
                    continue


            sql_list.append({
                "name": item["name"],
                "sql": item["sql"].format(db=db_name,table=table_name)
            })

    return sql_list