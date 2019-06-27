from disco.bot import Plugin
from disco.types.message import MessageEmbed
from datetime import datetime
from disco.util.chains import Chainable
import gevent

class Main(Plugin):
    @Plugin.command("profile", aliases = ["whois"], parser = True)
    @Plugin.add_argument("userID", type = str, nargs = "?")
    def on_profile_command(self, event):
        print("wip")

    @Plugin.command("adjustprofile", parser = True)
    @Plugin.add_argument("setting", type = str.lower, choices = ["callme", "gobyname", "description", "blurb",
       "timezone", "facts"], nargs = "?")
    def on_adjprf_command(self, event, args):
        PrefixHandler = self.bot.plugins.get("PrefixHandler")
        timeLimit = 30
        choices = ("`callme`, `blurb`, `timezone`, `facts`, `cancel`")

        print(args.setting)
        while args.setting is None:
            args.setting = PrefixHandler.prompt_for_arg(event, timeLimit, choices = choices)

        if args.setting in "timeout":
            pass
        elif args.setting in "cancel":
            event.msg.reply("**Prompt cancelled.**")
        elif args.setting in ("callme" or "gobyname"):
            self.on_callme_setting(event)
        elif args.setting in ("description" or "blurb"):
            self.on_blurb_setting(event)
        elif args.setting in ("timezone"):
            self.on_timezone_setting(event)
        elif args.setting in ("facts"):
            self.on_facts_setting(event)

    def on_callme_setting(self, event):
        print('callme triggered')

    def on_blurb_setting(self, event):
        print('blurb triggered')

    def on_timezone_setting(self, event):
        print('timezone triggered')

    def on_facts_setting(self, event):
        print("facts triggered")


