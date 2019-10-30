from disco.bot import Plugin
from disco.types.user import Game, GameType, Status
import re
import gevent

class Boot(Plugin):
    @Plugin.listen("Ready")
    def on_ready(self, event):
        """Updates the status of the bot when started"""
        self.client.update_presence(Status.online, Game(type = GameType.watching, #pylint: disable=no-member
         name = "people make friends!"))

    @Plugin.listen("GuildCreate")
    def on_guild_join(self, event):
        mariadb = self.bot.plugins.get("mariadb_funcs")
        if not mariadb.check_guild_exists(event.guild.id):
            mariadb.make_server(event.guild.id)