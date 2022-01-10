from game.classes import Room, Object, Player, Game
from game.data import room_data, object_data, player_data

game = Game(
    rooms={i: Room(**params) for i, params in room_data.items()},
    objects={i: Object(**params) for i, params in object_data.items()},
    player=Player(**player_data),
)
