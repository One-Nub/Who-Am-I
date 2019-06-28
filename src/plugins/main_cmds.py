from disco.bot import Plugin
from disco.types.message import MessageEmbed
from datetime import datetime
from disco.util.chains import Chainable

class Main(Plugin):
    @Plugin.command("profile", aliases = ["whois"], parser = True)
    @Plugin.add_argument("userID", type = str, nargs = "?")
    def on_profile_command(self, event):
        """(wip) Displays your profile for the world to see!"""
        print("wip")


    @Plugin.command("adjustprofile", parser = True)
    @Plugin.add_argument("setting", type = str.lower, choices = ["callme", "blurb",
       "timezone", "facts"], nargs = "?")
    def on_adjprf_command(self, event, args):
        """Change any of the settings on your profile!"""
        PrefixHandler = self.bot.plugins.get("PrefixHandler")
        timeLimit = 30
        choices = ("`callme` - Change the name the bot displays that you go by.\n"
            "`blurb` - Change your profile's description.\n"
            "`timezone` - Change your timezone\n"
            "`facts` - Change the interesting fact(s) on your profile.\n"
            "`cancel` - Cancel this prompt.")

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
        MariaDB = self.bot.plugins.get("mariadb_funcs")

        response = PrefixHandler.prompt_for_arg(event, timeLimit = 60)
        if response != "cancel":
            changeSetting = MariaDB.update_user_setting(event.author.id, 'call_me', response)
            if changeSetting == True:
                event.msg.reply("Your go by name has been updated!")
            else:
                event.msg.reply(changeSetting)

    def on_blurb_setting(self, event):
        PrefixHandler = self.bot.plugins.get("PrefixHandler")
        MariaDB = self.bot.plugins.get("mariadb_funcs")

        response = PrefixHandler.prompt_for_arg(event, timeLimit = 200)
        if response != "cancel":
            changeSetting = MariaDB.update_user_setting(event.author.id, 'usr_desc', response)
            if changeSetting == True:
                event.msg.reply("Your profile description has been updated!")
            else:
                event.msg.reply(changeSetting)

    def on_timezone_setting(self, event):
        PrefixHandler = self.bot.plugins.get("PrefixHandler")
        MariaDB = self.bot.plugins.get("mariadb_funcs")

        response = PrefixHandler.prompt_for_arg(event, timeLimit = 60)
        if response != "cancel":
            changeSetting = MariaDB.update_user_setting(event.author.id, 'timezone', response)
            if changeSetting == True:
                event.msg.reply("Your timezone has been updated!")
            else:
                event.msg.reply(changeSetting)

    def on_facts_setting(self, event):
        PrefixHandler = self.bot.plugins.get("PrefixHandler")
        MariaDB = self.bot.plugins.get("mariadb_funcs")

        response = PrefixHandler.prompt_for_arg(event, timeLimit = 200)
        if response != "cancel":
            changeSetting = MariaDB.update_user_setting(event.author.id, 'facts', response)
            if changeSetting == True:
                event.msg.reply("Your interesting fact has been updated!")
            else:
                event.msg.reply(changeSetting)

