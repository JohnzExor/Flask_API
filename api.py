from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "rest_db"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

def get_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/tables", methods=["GET"])
def show_tables():
    return make_response(jsonify(get_fetch("show tables")))

@app.route("/tables/<string:table>", methods=["GET"])
def select_table(table):
    return make_response(jsonify(get_fetch(f"select * from {table}")))

if __name__ == "__main__":
    app.run(debug=True)