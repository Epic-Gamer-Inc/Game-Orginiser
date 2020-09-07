from Rankings import *
from time import sleep
import dataset

db = dataset.connect('sqlite:///DataBase.db')
i = 1

for player in db['Players']:
    print(player['id'])

#while i:
#    posts = db['Players']
#    
#    print(posts)
#    sleep(10)

