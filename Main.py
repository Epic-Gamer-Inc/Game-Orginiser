from Rankings import *
from flask import *
import dataset

app = Flask(__name__)
db = dataset.connect('sqlite:///twittle.db')

app.secret_key = "kdJHGksdhjgldGHALKDJGHjg;98723048"

@app.route('/')
def main_get():
    if 'username' not in session:
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
    del session['username']
    return redirect('/')

@app.route('/login_post', methods=['post'])
def login_post():
    session['username'] = request.form['username']
    return redirect('/')

@app.route('/create_post', methods=['post'])
def create_post():
    post_dictionary = {
        'message' : request.form['message'],
        'username' : session['username'],
        'picture' : session['profile_picture_url']
    }

    db['posts'].insert(post_dictionary)

    return redirect('/')

@app.route('/profile')
def profile_get():
    username = request.args['username']

    filtered_posts = []
    for post in db['posts']:
        if post['username'] == username:
            filtered_posts.append(post)
    return render_template('Profile.html', filtered_posts=filtered_posts)

app.run(debug=True)