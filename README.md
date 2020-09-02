# Game-Orginiser

fool you read me

No, the you fool


_players = [
    'A',
    'B',
    'C',
    'D'
]
_playerRanks = {
    'A': 2500,
    'B': 1300,
    'C': 2600,
    'D': 1100
}

print(makeMatches(_players,_playerRanks))
for p in _players:
    print(catagorise(_playerRanks[p]))