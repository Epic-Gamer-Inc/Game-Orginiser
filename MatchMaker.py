from Rankings import *
from time import sleep
import dataset

db = dataset.connect('sqlite:///twittle.db')


posts = list(db['posts'])
print(posts)

