from flask import Flask, request, jsonify, render_template
from flask import redirect, url_for, abort, redirect
from flask_mysqldb import MySQL, MySQLdb
import argparse
import yaml

main = Flask(__name__, static_folder="main_static", template_folder="main_templates")

mysql = MySQL(main)


@main.route('/', methods=['GET'])
def home_page():
    return "Home page"


@main.route('/user_login', methods=['GET'])
def user_login():
    return render_template("user_login.html")


@main.route('/user_authentication', methods=['POST'])
def user_authentication():
    if request.method == 'POST':
        mobileno = request.form['mobileno']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT password FROM user WHERE mobileno = %s;", (mobileno,))
        val = cursor.fetchone()
        cursor.close()

    if val[0] == password:
        return f"login!!"
    else:
        return f"error!!"


@main.route('/new_user', methods=['GET'])
def new_user():
    return render_template("new_user.html")


@main.route('/new_user_registration', methods=['POST'])
def new_user_registration():
    if request.method == 'POST':
        emailid = request.form['emailid']
        mobileno = request.form['mobileno']
        password = request.form['password']
        dob = request.form['dob']

        cursor = mysql.connection.cursor()
        
        try:
            cursor.execute("INSERT INTO user (emailid, password, mobileno, dob) VALUES (%s, %s, %s, %s);", (emailid, password, mobileno, dob,))
        except MySQLdb._exceptions.OperationalError:
            return "age must be above 18!!"
        
        mysql.connection.commit()
        cursor.close()
    
    return redirect(url_for("user_login"))


@main.route('/admin_login', methods=['GET'])
def admin_login():
    return render_template("admin_login.html")


@main.route('/admin_authentication', methods=['POST'])
def admin_authentication():
    if request.method == 'POST':
        uid = request.form['uid']
        password = request.form['password']

    if uid == "admin" and password == "admin":
        return f"login!!"
    else:
        return f"error!!"


def read_config():
    with open("config.yaml", "r") as yaml_file:
        dbserver = yaml.safe_load(yaml_file)["dbserver"]
    return dbserver["user"], dbserver["password"], dbserver["host"], dbserver["database"]


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--user", default=None)
    args.add_argument("--password", default=None)
    args.add_argument("--host", default=None)
    args.add_argument("--db", default=None)
    parsed_args = args.parse_args()
    
    user = parsed_args.user
    password = parsed_args.password
    host = parsed_args.host
    db = parsed_args.db
    if (user is None and password is None 
        and host is None and db is None):
        user, password, host, db = read_config()

    main.config['MYSQL_HOST'] = host
    main.config['MYSQL_USER'] = user
    main.config['MYSQL_PASSWORD'] = password
    main.config['MYSQL_DB'] = db

    main.run(host='0.0.0.0', debug=True, port=2424)