from Rankings import *
from time import sleep
import dataset
import random
import string

db = dataset.connect('sqlite:///DataBase.db')
i = 1

#for player in db['Players']:
#    print(player['id'])


def addUser(username,passWord):
    userDict = {
        'id' : CreateId('Players'),
        'name':username,
        'passWord' : passWord,
        'team' : None,
        'profilePic' : 'Defult.png'
    }
    db['Players'].insert(userDict)

def CreateId(table):
    length = 6
    letters = string.ascii_lowercase
    id = ''.join(random.choice(letters) for i in range(length))
    while db[table].find_one(id=id):
        id = ''.join(random.choice(letters) for i in range(length))
    return id

def CreateTeam(players,name):
    teamId = CreateId('Teams')
    teamDict = {
        'id' : teamId,
        'name' : name,
        'mmr' : 2500,
        'player0' : players[0],
        'player1' : players[1],
        'player2' : players[2],
        'player3' : players[3],
        'player4' : players[4]
    }
    db['Teams'].insert(teamDict)
    for player in players:
        print(player)
        p = {
            'id' : player,
            'team' : teamId
        }
        db['Players'].update(p,['id'])

players = ['ikjtjs','rixtun','pejule','qttdwn','lkezyw']
CreateTeam(players,'test')
#for i in range(5):
#    addUser(f'User{i}', f'pass{i}')

#while i:
#    posts = db['Players']
#    
#    print(posts)
#    sleep(10)

