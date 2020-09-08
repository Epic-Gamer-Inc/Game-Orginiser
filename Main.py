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

@app.route('/login_post', methods=['post'])
def login_post():
    db_user = db['Players'].find_one(name=request.form['username'])
    db_password = str(db_user['passWord'])
    typed_password = request.form['password']
    if db_password == typed_password:
        session['name'] = request.form['username']
        session['id'] = db_user['id']
        session['profilePic'] = db_user['profilePic']
        return redirect('/')
    else:
        return "Invalid Password"


@app.route('/set_picture')
def set_picutre_get():
    return render_template('setpicture.html')

@app.route('/set_picture_post', methods=['post'])
def set_picutre_post():
    file = request.files['file']
    filename_to_save = 'static/uploads/' + file.filename
    file.save(filename_to_save)
    session['profilePic'] = upDatePfp(filename_to_save, session['id'])

    return redirect("/")

@app.route('/logout')
def logout_get():
    del session['name']
    return redirect('/')

@app.route('/create_account')
def create_account_get():
    return render_template('create_account.html')

@app.route('/create_account_post', methods=['post'])
def create_account_post():
    addUser(request.form['makeusername'],request.form['makepassword'])
    return redirect('/login')

@app.route('/profile')
def profile_get():
    return render_template('Profile.html', filtered_posts='')

@app.route('/create_team')
def create_team():
    return render_template('create_team.html')

@app.route('/create_team_post', methods=['post'])
def create_team_post():
    members = []
    player1 = request.form['P1'].split('#')
    player1 = player1[1]
    player2 = request.form['P2'].split('#')
    player2 = player2[1]
    player3 = request.form['P3'].split('#')
    player3 = player3[1]
    player4 = request.form['P4'].split('#')
    player4 = player4[1]

    members.append(session['id'])
    members.append(player1)
    members.append(player2)
    members.append(player3)
    members.append(player4)
    CreateTeam(members, request.form['teamName'])
    return redirect('/')

app.run(debug=True)