from disco.bot import Plugin
from disco.bot.command import Command, CommandEvent
from disco.types.user import Game, GameType, Status
import re

class Boot(Plugin):
    @Plugin.listen("Ready")
    def on_ready(self, event):
        self.client.update_presence(Status.online, Game(type = GameType.watching, #pylint: disable=no-member
         name = "people make friends!"))

class PrefixHandler(Plugin):
    @Plugin.listen("MessageCreate")
    def on_message_send(self, event):
        botAccount = event.message.author.bot
        firstWord = event.message.content.partition(" ")[0]
        prefix = self.get_prefix()
        mention = self.get_mention()

        if (self.find_prefix(firstWord)) and not (botAccount):
            self.run_command(event, prefix)
        elif (self.find_mention(firstWord)) and not (botAccount):
            self.run_command(event, mention)

    def get_prefix(self):
        prefix = ">"
        return prefix

    def find_prefix(self, firstWord):
        prefix = self.get_prefix()
        if prefix in firstWord[:len(prefix)]:
            return True
        else:
            return False

    def get_mention(self):
        mention = "<@{0}>".format(self.state.me.id)
        return mention

    def find_mention(self, firstWord):
        mention = self.get_mention()
        if mention in firstWord:
            return True
        else:
            return False

    def get_all_commands(self):
        command_list = []
        append = command_list.append

        for plugin in self.bot.plugins.values():
            for command in plugin.commands:
                append(command)
        return command_list

    def get_command_triggers(self, command):
        return getattr(command, "triggers")

    def run_command(self, event, prefix):
        msgContent = event.message.content[len(prefix):].lstrip()
        commandName = msgContent.partition(" ")[0]

        for command in self.get_all_commands():
            for val in self.get_command_triggers(command):
                if commandName in val:
                    command.execute(CommandEvent(command, event.message,
                     re.search(command.compiled_regex, msgContent)))
