from flask import Blueprint, render_template, request
import pymysql
from app.inspect.inspect_engine import load_inspect_sql,get_db_version
from flask import render_template, send_file
import datetime
import os
from flask import session


table_bp = Blueprint('table_bp', __name__, url_prefix='/tables')


@table_bp.route('/<host>/<int:port>/<db_name>')
def list_tables(host, port, db_name):
    user = request.args.get('user')
    password = request.args.get('password')

    conn = pymysql.connect(host=host,
                           port=port,
                           user=user,
                           password=password,
                           database=db_name,
                           connect_timeout=5,  # 连接超时
                           read_timeout=10,  # 查询执行超时（10秒）
                           write_timeout=10
                           )
    cursor = conn.cursor()

    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]

    conn.close()

    return render_template('tables.html',
                           tables=tables,
                           host=host,
                           port=port,
                           db_name=db_name,
                           user=user,
                           password=password)


@table_bp.route('/<host>/<int:port>/<db_name>/<table_name>/inspect', methods=['GET', 'POST'])
def table_inspect(host, port, db_name, table_name):

    user = request.args.get('user')
    password = request.args.get('password')

    sql_result = []

    if request.method == 'POST':

        inspect_type = request.form.get('inspect_type')
        sql_script = request.form.get('sql_script')

        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name
        )

        cursor = conn.cursor()

        sql_list = []

        # YAML巡检
        db_version = get_db_version(conn)
        if inspect_type in ["ops", "dev"]:
            sql_list = load_inspect_sql(inspect_type, db_name, table_name, db_version)

        # 手工SQL
        elif sql_script:
            sql_list = [{
                "name": "手动SQL",
                "sql": sql_script
            }]

        for item in sql_list:

            sql = item["sql"]

            try:
                cursor.execute(sql)

                columns = []
                if cursor.description:
                    columns = [desc[0] for desc in cursor.description]

                result = cursor.fetchall()

                sql_result.append({
                    "name": item["name"],
                    "sql": sql,
                    "columns": columns,
                    "result": result
                })

            except Exception as e:
                sql_result.append({
                    "name": item["name"],
                    "sql": sql,
                    "result": str(e)
                })

        conn.close()
        session['inspect_result'] = sql_result

    return render_template(
        "table_inspect.html",
        host=host,
        port=port,
        db_name=db_name,
        table_name=table_name,
        user=user,
        password=password,
        sql_result=sql_result
    )




@table_bp.route('/<host>/<int:port>/<db_name>/<table_name>/export_report', methods=['POST'])
def export_report(host, port, db_name, table_name):
    from flask import session, render_template, send_file
    import datetime
    import os

    sql_result = session.get('inspect_result')
    print(sql_result)
    if not sql_result:
        return "请先执行巡检！"

    html = render_template(
        "inspect_report.html",
        host=host,
        port=port,
        db_name=db_name,
        table_name=table_name,
        sql_result=sql_result,
        time=datetime.datetime.now()
    )

    filename = f"inspect_report_{table_name}.html"
    filepath = os.path.join(os.getcwd(), filename)  # 当前工作目录

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return send_file(filepath, as_attachment=True)