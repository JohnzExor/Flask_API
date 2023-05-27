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

#GET
@app.route("/tables", methods=["GET"])
def show_tables():
    return make_response(jsonify(get_fetch("show tables")))

@app.route("/tables/<string:table>", methods=["GET"])
def select_table(table):
    return make_response(jsonify(get_fetch(f"select * from {table}")))

@app.route("/tables/<string:table>/<int:id>", methods=["GET"])
def select_id(table, id):
    return make_response(jsonify(get_fetch(f"select * from {table} where id='{id}'")))

#POST
@app.route("/tables/students/add/<int:id>", methods=["POST"])
def add_student(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    last_name = info["last_name"]
    first_name = info["first_name"]
    subjects_id = info["subjects_id"]
    query = "insert into students values(%s, %s, %s, %s)"
    cur.execute(query, (id, last_name, first_name, subjects_id))
    mysql.connection.commit()
    row_changes = cur.rowcount
    cur.close()
    return make_response(jsonify({"Message": "Added Succesfully", "Row changes": row_changes}))




if __name__ == "__main__":
    app.run(debug=True)