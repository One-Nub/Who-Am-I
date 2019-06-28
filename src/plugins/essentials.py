from disco.bot import Plugin
from disco.bot.command import Command, CommandEvent
from disco.types.user import Game, GameType, Status
from disco.util.chains import Chainable
from disco.types.message import MessageEmbed
import re
import gevent

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

        if not event.channel.is_dm:
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

    def get_user_response(self, event):
        nextmsg = self.wait_for_event("MessageCreate")
        while nextmsg.get().author.id != event.author.id:
            nextmsg = self.wait_for_event("MessageCreate")
        return nextmsg.get().content

    def prompt_for_arg(self, event, timeLimit, choices = None):
        if choices:
            argsEmbed = MessageEmbed()
            argsEmbed.title = "Choices, choices..."
            argsEmbed.description = "**Please choose one of these options to configure!**\n\n{}".format(choices)
            argsEmbed.set_footer(text = "This prompt will self-cancel in {} seconds".format(timeLimit))
            argsEmbed.color = 0x8DD0E1
            botprompt = event.msg.reply(embed = argsEmbed)
        else:
            promptEmbed = MessageEmbed()
            promptEmbed.title = "Please input now what you want this field to be!"
            promptEmbed.description = "Or say **`cancel`** if you changed your mind."
            promptEmbed.color = 0x8DD0E1
            promptEmbed.set_footer(text = "This prompt will self-cancel in {} seconds".format(timeLimit))
            botprompt = event.msg.reply(embed = promptEmbed)
                #This I can either keep generic, or customize it before the call in the other files.

        try:
            with gevent.Timeout(timeLimit, TimeoutError):
                response = self.get_user_response(event)
                Chainable.chain(botprompt, response) #I honestly can't tell if this "Chainable" thing works or not
                    #It's supposed to run those objects in order one by one rather than in sync.
        except TimeoutError:
            event.msg.reply("Timeout limit of `{0} seconds` reached, prompt cancelled.".format(timeLimit))
            return "timeout"

        if choices:
            if response.lower() in choices:
                return response.lower()
            else:
                event.msg.reply("That option was invalid, please choose a correct value!")
                return None
        else:
            lowerResponse = response.strip()
            if lowerResponse.lower() == "cancel":
                event.msg.reply("**Prompt cancelled.**")
                return "cancel"
            else:
                return response
