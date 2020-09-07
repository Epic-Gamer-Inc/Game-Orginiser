from Rankings import *
from Database import *
from flask import *
import dataset
import random
import string

app = Flask(__name__)
db = dataset.connect('sqlite:///DataBase.db')

app.secret_key = "kdJHGksdhjgldGHALKDJGHjg;98723048"

@app.route('/')
def main_get():
    if 'name' not in session:
        return redirect('/login')
    return render_template("Main.html", posts=db['posts'])

@app.route('/login')
def login_get():
    return render_template('Login.html')

@app.route('/set_picture')
def set_picutre_get():
    return render_template('setpicture.html')

@app.route('/set_picture_post', methods=['post'])
def set_picutre_post():
    file = request.files['file']
    filename_to_save = 'static/uploads/' + file.filename
    file.save(filename_to_save)
    upDatePfp(filename_to_save, session['id'])
    return redirect("/")

@app.route('/logout')
def logout_get():
    del session['name']
    return redirect('/')

@app.route('/login_post', methods=['post'])
def login_post():
    db_user = db['Players'].find_one(name=request.form['username'])
    db_password = str(db_user['passWord'])
    typed_password = request.form['password']
    if db_password == typed_password:
        session['name'] = request.form['username']
        session['id'] = db_user['id']
        return redirect('/')
    else:
        return "Invalid Password"


@app.route('/create_account')
def create_account_get():
    return render_template('create_account.html')

@app.route('/create_account_post', methods=['post'])
def create_account_post():
    addUser(request.form['makeusername'],request.form['makepassword'])
    return redirect('/login')

@app.route('/profile')
def profile_get():
    username = request.args['name']
    filtered_posts = []
    return render_template('Profile.html', filtered_posts=filtered_posts)

app.run(debug=True)