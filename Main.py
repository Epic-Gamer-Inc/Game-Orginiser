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

    session['profile_picture_url'] = filename_to_save

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

@app.route('/create_post', methods=['post'])
def create_post():
    post_dictionary = {
        'message' : request.form['message'],
        'username' : session['name'],
        'picture' : session['profilePic']
    }

    db['posts'].insert(post_dictionary)

    return redirect('/')

@app.route('/profile')
def profile_get():
    username = request.args['name']

    filtered_posts = []
    for post in db['posts']:
        if post['username'] == username:
            filtered_posts.append(post)
    return render_template('Profile.html', filtered_posts=filtered_posts)

app.run(debug=True)