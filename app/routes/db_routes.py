from flask import Blueprint, render_template, request
import pymysql

db_bp = Blueprint('db_bp', __name__, url_prefix='/databases')

@db_bp.route('/<host>/<int:port>')
def list_databases(host, port):
    user = request.args.get('user')
    password = request.args.get('password')
    conn = pymysql.connect(host=host, port=port, user=user, password=password)
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    dbs = [db[0] for db in cursor.fetchall()]
    conn.close()
    return render_template('databases.html', databases=dbs, host=host, port=port, user=user, password=password)