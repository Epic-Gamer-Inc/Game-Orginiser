from Rankings import *
from time import sleep
import dataset
import random
import string
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

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
        'mmr' : random.randrange(2000,3000),
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

def updateRanks(newMmr, newSigma, teamId):
    p = {
            'id' : teamId,
            'mmr' : newMmr,
            'sigma' : newSigma
        }
    db['Teams'].update(p,['id'])

def GetFullName(id):
    try:    
        i = db['Players'].find_one(id = id)
        name =  i['name']
        return f'{name}#{id}'
    except:
        return 'error bad id'

def GetTeamName(id):
    try:
        i = db['Teams'].find_one(id = id)
        return i['name']
    except: 
        return 'error bad id'

def GetQueue():
    queue = []
    queueRanks = {}
    queue_rows = db['Queue']
    #print(i)
    for queue_item in queue_rows:
        #print(c)
        team = db['Teams'].find_one(id = str(queue_item['team']))
        if team is None:
            raise Exception("There is no team with an id of", queue_item['team'])
        queue.append(team['id'])
        queueRanks[team['id']] = team['mmr']
        queue_rows.delete(id = queue_item['id'])
    return queue, queueRanks

def joinQueue(teamId):
    queue = db['Queue']
    dic = {
        'team' : teamId
    }
    queue.insert(dic)

def leaveQueue(teamId):
    db['Queue'].delete(team=teamId)

def addMatches(matches):
    matchDb = db['Matches']
    for match in matches:
        dic = {
            'team1': match[0],
            'team2': match[1]
        }
        matchDb.insert(dic)


def Do1v1(winId,looseId,draw):
    teamDb = db['Teams']
    wTeam = teamDb.find_one(id = winId)
    lTeam = teamDb.find_one(id = looseId)
    wRank = (wTeam['mmr'],wTeam['sigma'])
    lRank = (lTeam['mmr'],lTeam['sigma'])
    thing = run1v1(wRank,lRank,draw)
    updateRanks(thing[0][0],thing[0][1],winId)
    updateRanks(thing[1][0],thing[1][1],looseId)



if __name__ == '__main__':
    #print(CreateId('Players'))
    #print(GetFullName('8040'))
    #print(GetTeamName('2399'))
    #joinQueue(CreateId('Players'))
    #leaveQueue('12345')
    #print(GetQueue())
    Do1v1(2399,6228,False)
    pass
