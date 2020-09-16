from Database import *
from Rankings import *
from time import sleep
runQueue = True

queue = []
queueDict = {}
matches = []
while runQueue:
    gq = GetQueue()
    print(gq)
    print(matches,queue, queueDict)
    gq[1].update(queueDict)
    print(gq[1])
    mm =  makeMatches(gq[0] + queue, gq[1])
    matches = mm[0]
    queue = mm[1]
    queueDict = mm[2]
    addMatches(matches)
    sleep(5)