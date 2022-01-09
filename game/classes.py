from dataclasses import dataclass, field


@dataclass
class Room:
    description: str
    exits: dict = field(default_factory=dict)


@dataclass
class Player:
    location: int
    inventory: list = field(default_factory=list)


class Game:
    def __init__(self, rooms, player):
        self.rooms = rooms
        self.player = player

    def process_command(self, command):
        exits = self.current_room.exits
        if command in ('north', 'south', 'west', 'east'):
            if command in exits:
                self.player.location = exits[command]

    @property
    def current_room(self):
        return self.rooms[self.player.location]
