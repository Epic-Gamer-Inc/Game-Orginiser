from Rankings import *
from flask import *
import dataset

app = Flask(__name__)
db = dataset.connect('sqlite:///twittle.db')

app.secret_key = "kdJHGksdhjgldGHALKDJGHjg;98723048"

@app.route('/')
def index_get():
    
    return render_template('Main.html')
    
app.run(debug=True)