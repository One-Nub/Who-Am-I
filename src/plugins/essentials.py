from disco.bot import Plugin
from disco.bot.command import Command, CommandEvent
from disco.types.user import Game, GameType, Status
import re

class Boot(Plugin):
    @Plugin.listen("Ready")
    def on_ready(self, event):
        """Updates the status of the bot when started"""
        self.client.update_presence(Status.online, Game(type = GameType.watching, #pylint: disable=no-member
         name = "people make friends!"))

class PrefixHandler(Plugin):
    @Plugin.listen("MessageCreate")
    def on_message_send(self, event):
        """Perform actions to run a command when a message is sent."""
        botAccount = event.message.author.bot
        firstWord = event.message.content.partition(" ")[0]
        firstWord = firstWord.lower()

        prefix = self.get_prefix()
        mention = self.get_mention()

        if (self.find_prefix(firstWord)) and not (botAccount):
            if not self.find_group(firstWord):
                self.run_command(event, prefix)
            else:
                self.run_command(event, prefix, group = True)
        elif (self.find_mention(firstWord)) and not (botAccount):
            if not self.find_group(firstWord):
                self.run_command(event, mention)
            else:
                self.run_command(event, mention, group = True)


    def get_prefix(self):
        prefix = ">"
        return prefix

    def find_prefix(self, firstWord):
        prefix = self.get_prefix()
        if prefix == firstWord[:len(prefix)]:
            return True
        else:
            return False

    def get_mention(self):
        mention = "<@{0}>".format(self.state.me.id)
        return mention

    def find_mention(self, firstWord):
        mention = self.get_mention()
        if mention == firstWord:
            return True
        else:
            return False

    def get_groups(self):
        group_list = []
        append = group_list.append
        for command in self.get_all_commands():
            group = getattr(command, "group")
            if group:
                append(group)
        return group_list

    def find_group(self, firstWord):
        default = False
        for group in self.get_groups():
            if group.lower() == firstWord:
                return True
        return default

    def get_all_commands(self):
        command_list = []
        append = command_list.append

        for plugin in self.bot.plugins.values():
            for command in plugin.commands:
                append(command)
        return command_list

    def get_command_triggers(self, command):
        return getattr(command, "triggers")

    def get_cmd_docstring(self, command):
        return command.get_docstring()

    def run_command(self, event, prefix, group = False):
        msgContent = event.message.content[len(prefix):].lstrip()
        firstWord = msgContent.partition(" ")[0]
        restOfPartition = msgContent.partition(" ")[2]
        secondWord = restOfPartition.partition(" ")[0]

        firstWord = firstWord.lower()
        secondWord = secondWord.lower()

        for command in self.get_all_commands():
            for trigger in self.get_command_triggers(command):
                if (not group) and (firstWord == trigger.lower()):
                    command.execute(CommandEvent(command, event.message,
                    re.search(command.compiled_regex, msgContent)))
                elif (group) and (secondWord == trigger.lower()):
                    command.execute(CommandEvent(command, event.message,
                    re.search(command.compiled_regex, msgContent)))
