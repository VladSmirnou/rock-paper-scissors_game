from typing import NewType


GameId = NewType('GameId: str', str)
GamesWon = NewType('GamesWon: int', int)
GamesLost = NewType('GamesLost: int', int)

SavedGames = list[tuple[GameId, GamesLost, GamesWon]]
