from disco.bot import Plugin
from disco.types.message import MessageEmbed
from datetime import datetime
from disco.util.chains import Chainable

class Main(Plugin):
    @Plugin.command("profile", aliases = ["whois"], parser = True)
    @Plugin.add_argument("userID", type = str, nargs = "?")
    def on_profile_command(self, event):
        print("wip")

    @Plugin.command("adjustprofile", parser = True)
    @Plugin.add_argument("setting", type = str.lower, choices = ["callme", "blurb",
       "timezone", "facts"], nargs = "?")
    def on_adjprf_command(self, event, args):
        PrefixHandler = self.bot.plugins.get("PrefixHandler")
        timeLimit = 30
        choices = ("`callme`, `blurb`, `timezone`, `facts`, `cancel`")

        while args.setting is None:
            args.setting = PrefixHandler.prompt_for_arg(event, timeLimit, choices = choices)
        if args.setting == "timeout":
            print("timeout")
        elif args.setting == "cancel":
            event.msg.reply("**Prompt cancelled.**")
        elif args.setting == ("callme"):
            self.on_callme_setting(event)
        elif args.setting == ("blurb"):
            self.on_blurb_setting(event)
        elif args.setting == ("timezone"):
            self.on_timezone_setting(event)
        elif args.setting == ("facts"):
            self.on_facts_setting(event)

    def on_callme_setting(self, event):
        PrefixHandler = self.bot.plugins.get("PrefixHandler")
        response = PrefixHandler.prompt_for_arg(event, timeLimit = 60)
        if response != "cancel":
            event.msg.reply(response)

    def on_blurb_setting(self, event):
        PrefixHandler = self.bot.plugins.get("PrefixHandler")
        response = PrefixHandler.prompt_for_arg(event, timeLimit = 200)
        if response != "cancel":
            event.msg.reply(response)

    def on_timezone_setting(self, event):
        PrefixHandler = self.bot.plugins.get("PrefixHandler")
        response = PrefixHandler.prompt_for_arg(event, timeLimit = 60)
        if response != "cancel":
            event.msg.reply(response)

    def on_facts_setting(self, event):
        PrefixHandler = self.bot.plugins.get("PrefixHandler")
        response = PrefixHandler.prompt_for_arg(event, timeLimit = 200)
        if response != "cancel":
            event.msg.reply(response)
