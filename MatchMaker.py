from Database import *
from Rankings import *
from time import sleep
runQueue = True

queueDict = {}
matches = []
while runQueue:
    
    matches,queue = makeMatches(GetQueue()[0],GetQueue()[1])
    
    sleep(5)