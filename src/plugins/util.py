from disco.bot import Plugin
from disco.types.message import MessageEmbed
from datetime import datetime

class Utilities(Plugin):
    @Plugin.command("help", aliases = ["temp"])
    def on_help_command(self, event):
        """Displays a list of my commands and what they do."""
        helpEmbed = MessageEmbed()
        helpEmbed.title = "**Need some help?**"
        helpEmbed.timestamp = datetime.utcnow().isoformat()

        PrefixHandler = self.bot.plugins.get("PrefixHandler") #This gets the PrefixHandler from the other file
        for plugin in self.bot.plugins.values():
            if plugin.commands:
                commandFormat = ""
                for command in plugin.commands:
                    name = command.name
                    desc = PrefixHandler.get_cmd_docstring(command)
                    commandFormat += "`{0}` ➙ `{1}` \n".format(name, desc)
                helpEmbed.add_field(name = plugin.name, value = commandFormat, inline = False)
        event.msg.reply(embed = helpEmbed)


