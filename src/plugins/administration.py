from disco.bot import Plugin
from disco.types.message import MessageEmbed
from disco.types.permissions import Permissions
from datetime import datetime

class Administration(Plugin):
    @Plugin.command("setprefix", aliases = ["updateprefix", "changeprefix"], parser = True)
    @Plugin.add_argument("prefix", type = str, nargs = "?")
    def on_setprefix_command(self, event, args):
        """Updates the server's prefix. The prefix can be retrieved later in the help command"""
        channel = event.channel
        if channel.get_permissions(event.msg.author).can(Permissions.MANAGE_GUILD):
            mariadb = self.bot.plugins.get("mariadb_funcs")
            PrefixHandler = self.bot.plugins.get("PrefixHandler")
            if args.prefix:
                tryUpdate = mariadb.update_server_prefix(event.guild.id, args.prefix)
                if tryUpdate == True:
                    event.msg.reply("Prefix successfully updated to `{}`".format(args.prefix))
                else:
                    event.msg.reply("Error: ```{}```".format(args.prefix))
            else:
                prefix = PrefixHandler.prompt_for_arg(event, timeLimit = 30, fieldName = "server prefix")
                if prefix != "cancel":
                    tryUpdate = mariadb.update_server_prefix(event.guild.id, args.prefix)
                    if tryUpdate == True:
                        event.msg.reply("Prefix successfully updated to `{}`".format(prefix))
                    else:
                        event.msg.reply("Error: ```{}```".format(prefix))
