from disco.bot import Plugin
from disco.types.user import Game, GameType, Status

class Boot(Plugin):
    @Plugin.listen("Ready")
    def on_ready(self, event):
        self.client.update_presence(Status.online, Game(type = GameType.watching, #pylint: disable=no-member
         name = "people make friends!"))
