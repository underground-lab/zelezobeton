from game.classes import Room, Player, Game
from game.data import room_data, player_data

game = Game(
    rooms={i: Room(**params) for i, params in room_data.items()},
    player=Player(**player_data),
)
