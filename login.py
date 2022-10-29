from flask import Flask, render_template, request, jsonify, session, redirect
import pymysql


db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "{DB_USERNAME}",
    "password": "{DB_PASSWORD}",
    "db": "{DB_NAME}",
    "charset": "utf8"
}

try:
    conn = pymysql.connect(**db_settings)
    cur = conn.cursor()
except Exception as e:
    print(e)


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World"

@app.route('/user/register', methods = ["POST"])
def user_register():
    if request.method == 'POST':   
        json = request.get_json()
        user_id = json["user_id"]
        user_name = json["user_name"]
        password = json["password"]     
     
        sequence = (user_id, user_name, password)
        print(sequence)
        formula = "INSERT INTO user_db.user_info(user_id, user_name, password) VALUES (%s, %s, %s);"
        cur.execute(formula, sequence)
        conn.commit()
        return str(sequence) + "Done!"
        

app.run(port= 8080)