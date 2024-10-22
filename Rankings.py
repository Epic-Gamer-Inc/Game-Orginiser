from trueskill import *
import json

def FillFile(): #use to fill a json file for testing porposes
    try: 
        with open('Ranks.txt') as f:
            f = json.loads(f.read())
            playerRanks = f[0]
            players = f[1]
            return playerRanks,players
    except Exception as E:
        print(E)
        playerRanks = {}
        players = []
        playerName = input('PlayerName: ')
        while playerName:
            mmr = int(input('PlayerMMR: '))
            playerName = playerName.lower()
            if playerName in playerRanks:
                print('Player Already In')
            else: 
                playerRanks[playerName] = mmr
                players.append(playerName)
            playerName = input('PlayerName: ')
        try:
            with open('Ranks.txt','w') as f:
                f.write(json.dumps((playerRanks,players)))
            return playerRanks,players
        except Exception as a:
            print(a)

def makeMatches(players,playerRanks): #creates matches out of an list/dictionary based off of rank will return [] if len(players) is not even
    matches = []
    queue = []
    queueRanks = {}
    usedPlayers = []
    for p1 in players:
        if p1 not in usedPlayers:
            name1 = p1
            oddsOfDraw = .25
            bestMatch = name1
            usedPlayers.append(name1)
            p1 = Rating(playerRanks[p1]/100)
            for p2 in players:
                if name1 != p2 and p2 not in usedPlayers:
                    name2 = p2
                    p2 = Rating(playerRanks[p2]/100)
                    q = quality_1vs1(p1,p2)
                    if q > oddsOfDraw:
                        bestMatch = tuple((name1,name2))
                        oddsOfDraw = q
            if type(bestMatch) == tuple:
                matches.append(bestMatch)
                usedPlayers.append(bestMatch[1])
            else:
                queue.append(bestMatch)
                queueRanks[bestMatch] = playerRanks[bestMatch]
    #print(queueRanks)
    return matches, queue, queueRanks

def catagorise(mmr): #returns the name of the rank based off mmr
    try:
        with open('RankNames.txt') as f:
            for line in f:
                line = line.split()
                if mmr < int(line[1]):
                    return f'{line[0][:-1]}{line[0][-1]}'
    except:
        return 'Undefined'

def run1v1(winner, looser, draw):
    w = Rating(winner[0],winner[1])
    l = Rating(looser[0],looser[1])
    rw,rl = rate_1vs1(w,l,draw)
    w = (rw.mu,rw.sigma)
    l = (rl.mu,rl.sigma)
    return w,l

if __name__ == "__main__":
    '''
    _playerRanks = {}
    _players = []
    _playerRanks,_players = FillFile()
    print(makeMatches(_players,_playerRanks))
    print(catagorise(3300))
    '''
    winner = (2500,8.333333333333334)
    looser = (2600,8.333333333333334)
    print(run1v1(winner,looser,False))
    
    print(Rating(2500).sigma)