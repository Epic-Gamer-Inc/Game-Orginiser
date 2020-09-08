from Rankings import *
from time import sleep
import dataset
import random
import string
from sqlalchemy.sql import text

db = dataset.connect('sqlite:///DataBase.db')

def addUser(username,passWord):
    userDict = {
        'id' : CreateId('Players'),
        'name':username,
        'passWord' : passWord,
        'team' : '',
        'profilePic' : 'static/uploads/Defult.png'
    }
    db['Players'].insert(userDict)

def CreateId(table):
    length = 4
    letters = string.digits
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
        'sigma' : 8.333333333333334,
        'player0' : players[0],
        'player1' : players[1],
        'player2' : players[2],
        'player3' : players[3],
        'player4' : players[4],
        
    }
    db['Teams'].insert(teamDict)
    #print(list(db['Teams']))
    for player in players:
        #print(player)
        p = {
            'id' : player,
            'team' : teamId
        }
        db['Players'].update(p,['id'])

def upDatePfp(imageName,user):
    p = {
            'id' : user,
            'profilePic' : imageName
        }
    db['Players'].update(p,['id'])

def updateRanks(new,teamId):
    p = {
            'id' : teamId,
            'mmr' : new
        }
    db['Teams'].update(p,['id'])

def GetFullName(id):
    i = db['Players'].find_one(id)
    name =  i['name']
    return f'{name}#{id}'

def getTeamName(id):
    j = db['Teams'].find_one(text(id))
    name = j['name']
    return name

if __name__ == '__main__':
    print(CreateId('Players'))
