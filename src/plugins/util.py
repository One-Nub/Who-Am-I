from disco.bot import Plugin
from disco.types.message import MessageEmbed
from datetime import datetime

class Utilities(Plugin):
    @Plugin.command("help")
    def on_help_command(self, event):
        """Displays a list of my commands and what they do."""
        helpEmbed = MessageEmbed()
        helpEmbed.title = "**Need some help?**"
        helpEmbed.description = "Find me on github: https://github.com/One-Nub/Who-Am-I"
        helpEmbed.timestamp = datetime.utcnow().isoformat()
        helpEmbed.color = 0x8DD0E1

        PrefixHandler = self.bot.plugins.get("PrefixHandler") #This gets the PrefixHandler from the other file
        for plugin in self.bot.plugins.values():
            if plugin.commands:
                commandFormat = ""
                for command in plugin.commands:
                    name = command.name
                    desc = PrefixHandler.get_cmd_docstring(command)
                    if desc is '':
                        desc = "No docstring was found."
                    commandFormat += "`{0}` ➙ `{1}` \n".format(name, desc)
                helpEmbed.add_field(name = plugin.name, value = commandFormat, inline = False)
        event.msg.reply(embed = helpEmbed)

    @Plugin.command("info")
    def on_info_command(self, event):
        """Displays some info about the bot, or me!"""
        infoEmbed = MessageEmbed()
        github = "https://github.com/One-Nub/Who-Am-I"
        myPfpImg = "https://i.lensdump.com/i/WDsOXb.png"
        botPfpImg = "https://i.lensdump.com/i/WDs4G5.png"

        infoEmbed.title = "Welcome to **Who Am I**!"
        infoEmbed.url = github
        infoEmbed.color = 0x8DD0E1
        infoEmbed.description = "Hey there! This bot was created for the June 2019 Discord Hackathon!"
        infoEmbed.set_thumbnail(url = botPfpImg)
        infoEmbed.set_author(name = "Nub#8399", icon_url = myPfpImg)
        infoEmbed.timestamp = datetime.utcnow().isoformat()

        infoEmbed.add_field(name = "What is/was this Hackathon?",
            value = ("This was a week where developers, such as myself, would create either a bot of some sort, "
        "or something creative (art, music, etc...), "
        "and we would then submit our creations by the end of the week!"),
            inline = False)

        infoEmbed.add_field(name = "So what does this bot do?",
        value = ("This bot is meant to make it easier to learn about people and share info about yourself! \n"
            "This is done by letting users give info to the bot & then displaying that info with a simple command!"),
            inline = False)

        infoEmbed.add_field(name = "View my github here!", value = github, inline = False)
        event.msg.reply(embed = infoEmbed)

    @Plugin.command("ping", aliases = ["pong"])
    def on_ping_command(self, event):
        """Responds with 'Pong!' if the bot is online"""
        event.msg.reply("Pong!")
