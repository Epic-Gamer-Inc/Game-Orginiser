from Rankings import *
from Database import *
from flask import *
import dataset
import random
import string
from sqlalchemy.sql import text

app = Flask(__name__)
db = dataset.connect('sqlite:///DataBase.db')

app.secret_key = "kdJHGksdhjgldGHALKDJGHjg;98723048"

@app.route('/')
def main_get():
    if 'name' not in session:
        return redirect('/login')
    player = db['Players'].find_one(name=session['name'])
    return render_template("Main.html", posts=db['posts'], player=player)

@app.route('/login')
def login_get():
    return render_template('Login.html')

@app.route('/login_post', methods=['post'])
def login_post():
    try: 
        db_user = db['Players'].find_one(name=request.form['username'])
        db_password = str(db_user['passWord'])
        typed_password = request.form['password']
        if db_password == typed_password:
            session['name'] = request.form['username']
            session['id'] = db_user['id']
            session['profilePic'] = db_user['profilePic']
            return redirect('/')
        else:
            flash('Incorrect Password')
            return redirect('/login')
    except:
        flash('Invalid Username')
        return redirect('/login')

@app.route('/set_picture')
def set_picutre_get():
    return render_template('setpicture.html')

@app.route('/set_picture_post', methods=['post'])
def set_picutre_post():
    file = request.files['file']
    filename_to_save = 'static/uploads/' + file.filename
    file.save(filename_to_save)
    session['profilePic'] = filename_to_save
    
    upDatePfp(filename_to_save, session['id'])

    return redirect("/")

@app.route('/logout')
def logout_get():
    session.clear()
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
    db_user = db['Players'].find_one(name=session['name'])
    try:
        session['teamName'] = GetTeamName(db_user['team'])
        db_team = db['Teams'].find_one(id=db_user['team'])
        session['teamMembers'] = list([GetFullName(db_team['player0']),GetFullName(db_team['player1']),GetFullName(db_team['player2']),GetFullName(db_team['player3']),GetFullName(db_team['player4'])])
        session['teamRank'] = catagorise(db_team['mmr'])
        displayteam = True
        return render_template('Profile.html', displayteam=displayteam)
    except:
        if 'teamName' in session:
            del session['teamName']
        displayteam = False
        return render_template('Profile.html', displayteam=displayteam)

@app.route('/create_team')
def create_team():
    return render_template('create_team.html')

@app.route('/create_team_post', methods=['post'])
def create_team_post():
    try:
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
        db_user = db['Players'].find_one(name=session['name'])
        session['teamName'] = GetTeamName(db_user['team'])
        db_team = db['Teams'].find_one(id=db_user['team'])
        session['teamMembers'] = list([GetFullName(db_team['player0']),GetFullName(db_team['player1']),GetFullName(db_team['player2']),GetFullName(db_team['player3']),GetFullName(db_team['player4'])])
        session['teamRank'] = catagorise(db_team['mmr'])
        return redirect('/')
    except:
        flash('Invalid Users Entered')
        return render_template('create_team.html')

@app.route('/find_match')
def find_match():
    player = db['Players'].find_one(name=session['name'])
    teamid = player['team']
    team = db['Teams'].find_one(id=teamid)
    mmr = catagorise(team['mmr'])
    membersList = list([GetFullName(team['player0']),GetFullName(team['player1']),GetFullName(team['player2']),GetFullName(team['player3']),GetFullName(team['player4'])])
    
    ChangeStatus('Queing',teamid)

    if team['status'] != 'Queing':
        joinQueue(teamid)

    if db['Matches'].find_one(team1=teamid):
        return redirect('/results')
    elif db['Matches'].find_one(team2=teamid):
        return redirect('/results')

    return render_template('find_game.html', player=player, team=team,mmr=mmr, membersList=membersList)

@app.route('/results')
def result():
    player = db['Players'].find_one(name=session['name'])
    teamid = player['team']
    team = db['Teams'].find_one(id=teamid)
    ChangeStatus('Not Queing',teamid)
    return render_template('results.html')

@app.route('/results_post', methods=['post'])
def results_post():
    player = db['Players'].find_one(name=session['name'])
    teamid = player['team']
    score1 = int(request.form['score1'])
    score2 = int(request.form['score2'])
    match = db['Matches'].find_one(team1=teamid)
    try:
        matchid = match['matchId']
    except:
        return redirect('/')
    if not match:
        match = db['Matches'].find_one(team2=teamid)
    if not match:
        raise Exception("NO MATCH WITH YOUR TEAMID")

    if score1 > score2:
        Do1v1(match['team1'], match['team2'], False)
        RemoveMatches(matchid)
    elif score1 < score2:
        Do1v1(match['team2'], match['team1'], False)
        RemoveMatches(matchid)
    else:
        Do1v1(match['team1'], match['team2'], True)
        RemoveMatches(matchid)
    return redirect('/')
app.run(debug=True)