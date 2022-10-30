from flask import Flask, render_template, request, jsonify, session, redirect
import pymysql


db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "{DB_USER}",
    "password": "{DB_PASSWORD}",
    "db": "user_db",
    "charset": "utf8"
}

try:
    conn = pymysql.connect(**db_settings)
    cur = conn.cursor()
except Exception as ex:
    print(ex)


app = Flask(__name__)


def check_user_login():
    return session.get('user_id')

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

        formula = "INSERT INTO user_db.user_info(user_id, user_name, password) VALUES (%s, %s, %s);"
        cur.execute(formula, sequence)
        conn.commit()
        return str(sequence) + "Done!"

@app.route('/user/login', methods = ["GET", "POST"])
def user_login():
    if request.method == "POST":
        json = request.get_json()
        user_id = json["user_id"]
        password = json["password"]
        sequence = (user_id, password)
        formula = "SELECT user_id FROM user_db.user_info WHERE user_id = %s AND password = %s;"
        cur.execute(formula, sequence)
        id_list = cur.fetchall()
    
      
        if id_list:
            return "success!"
        else:
            data = {"err_msg": "username or password is incorrect."}
            return data

  
  

app.run(port= 8080)