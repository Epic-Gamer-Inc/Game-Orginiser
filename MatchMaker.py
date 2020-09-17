from Database import *
from Rankings import *
from time import sleep
from pprint import pprint
runQueue = True

queue = []
queueDict = {}
matches = []
while runQueue:
    print('the entire queue is:')
    #pprint(list(db['Queue']))
    gq = GetQueue()
    print(queue)
    print("matches are")
    print(matches)
    gq[1].update(queueDict)
    mm =  makeMatches(gq[0] + queue, gq[1])
    matches = mm[0]
    queue = mm[1]
    queueDict = mm[2]
    addMatches(matches)
    sleep(5)