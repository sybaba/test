from flask import Blueprint, render_template
from app.models import instances
from app.inspect.inspect_engine import load_inspect_sql,get_db_version
from flask import Blueprint, render_template, request, session
import pymysql

instance_bp = Blueprint('instance_bp', __name__, url_prefix='/instances')

@instance_bp.route('/')
def list_instances():
    return render_template('instances.html', instances=instances)

# 实例批量巡检
@instance_bp.route('/inspect/<host>/<int:port>', methods=['POST'])
def instance_batch_inspect(host, port):

    user = request.form.get("user")
    password = request.form.get("password")
    inspect_type = request.form.get("inspect_type")

    sql_result = []

    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password
    )

    cursor = conn.cursor()

    # 获取数据库版本
    db_version = get_db_version(conn)

    # 获取所有库
    cursor.execute("show databases")
    db_list = [x[0] for x in cursor.fetchall()]

    for db in db_list:

        if db in ["information_schema", "performance_schema", "mysql", "sys"]:
            continue

        cursor.execute(f"use `{db}`")

        cursor.execute("show tables")
        tables = [x[0] for x in cursor.fetchall()]

        for table in tables:

            sql_list = load_inspect_sql(inspect_type, db, table, db_version)

            for item in sql_list:

                sql = item["sql"]

                try:
                    cursor.execute(sql)

                    columns = []
                    if cursor.description:
                        columns = [d[0] for d in cursor.description]

                    result = cursor.fetchall()

                    sql_result.append({
                        "db": db,
                        "table": table,
                        "name": item["name"],
                        "sql": sql,
                        "columns": columns,
                        "result": result
                    })

                except Exception as e:

                    sql_result.append({
                        "db": db,
                        "table": table,
                        "name": item["name"],
                        "sql": sql,
                        "result": str(e)
                    })

    conn.close()

    return render_template(
        "instances.html",
        instances=instances,
        sql_result=sql_result
    )
