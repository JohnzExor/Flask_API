from functools import wraps
from flask import Flask, make_response, jsonify, request, abort
from flask_mysqldb import MySQL
import secrets

api_key = secrets.token_hex(16)
print(f"API KEY: {api_key}")

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "rest_db"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["API_KEY"] = api_key
mysql = MySQL(app)

def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("API-Key")
        if api_key != app.config["API_KEY"]:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function

#GET
def get_fetch(query):
    try:
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"Error": str(e)}), 400)


@app.route("/tables", methods=["GET"])
@api_key_required
def show_tables():
    return get_fetch("Show tables")

@app.route("/tables/<string:table>", methods=["GET"])
@api_key_required
def select_table(table):
    return get_fetch(f"select * from {table}")

@app.route("/tables/<string:table>/<int:id>", methods=["GET"])
@api_key_required
def select_id(table, id):
    return get_fetch(f"select * from {table} where id='{id}'")

#POST
@app.route("/tables/students/<int:id>", methods=["POST"])
@api_key_required
def add_student(id):
    try:
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
        return make_response(jsonify({"Message": "Added Succesfully", "Row changes": row_changes}), 201)
    except Exception as e:
        return make_response(jsonify({"Error": str(e)}), 400)
    
#PUT
@app.route("/tables/students/<int:id>", methods=["PUT"])
@api_key_required
def update_student(id):
    try:
        cur = mysql.connection.cursor()
        info = request.get_json()
        last_name = info["last_name"]
        first_name = info["first_name"]
        subjects_id = info["subjects_id"]
        query = "update students set lastname=%s, firstname=%s, subjects_id=%s where id=%s"
        cur.execute(query, (last_name, first_name, subjects_id, id,))
        mysql.connection.commit()
        row_changes = cur.rowcount
        cur.close()
        return make_response(jsonify({"Message": "PUT Success", "Row changes": row_changes}))
    except Exception as e:
        return make_response(jsonify({"Error": str(e)}), 400)
    
#DELETE
@app.route("/tables/students/<int:id>", methods=["DELETE"])
@api_key_required
def delete_student(id):
    try:
        cur = mysql.connection.cursor()
        query = "delete from students where id=%s"
        cur.execute(query, (id,))
        mysql.connection.commit()
        row_changes = cur.rowcount
        cur.close()
        return make_response(jsonify({"Message": "Has been deleted successfully", "Row changes": row_changes}), 200)
    except Exception as e:
        return make_response(jsonify({"Error": str(e)}), 400)

if __name__ == "__main__":
    app.run(debug=True)