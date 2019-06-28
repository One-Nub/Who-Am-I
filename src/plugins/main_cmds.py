from disco.bot import Plugin
from disco.types.message import MessageEmbed
from datetime import datetime
from disco.util.chains import Chainable
from disco.types.base import UNSET
import re
import random

class Main(Plugin):
    @Plugin.command("profile", aliases = ["whois"], parser = True)
    @Plugin.add_argument("userID", type = str, nargs = "?")
    def on_profile_command(self, event, args):
        """Displays your profile for the world to see!"""
        mariadb = self.bot.plugins.get("mariadb_funcs")
        if args.userID:
            user = args.userID
            user = re.sub("[<@!>]", '', user)
        else:
            user = event.msg.author.id
        if mariadb.check_user_exists(user):
            usrSettings = mariadb.get_user_settings(user)
            userID = usrSettings[0]
            userObj = self.state.users.get(userID)
            userPFPLink = userObj.get_avatar_url()
            userGoBy = usrSettings[1]
            userDesc = usrSettings[2]
            userTimezone = usrSettings[3]
            userIntFacts = usrSettings[4]

            if userObj.presence is not UNSET:
                usrState =  userObj.presence.status
            else:
    	        usrState = "offline"

            profileEmbed = MessageEmbed()
            profileEmbed.title = "The amazing profile of {0}#{1} who is currently **{2}**!".format(userObj.username, userObj.discriminator, usrState)
            profileEmbed.set_thumbnail(url = userPFPLink)

            color = random.randint(0, 0xFFFFFF)
            profileEmbed.color = color

            if userDesc == None:
                profileEmbed.description = """This user hasn't set a description!
                Please run `@Who Am I#1225 adjustprofile blurb`"""
            else:
                profileEmbed.description = userDesc

            if userGoBy != None:
                profileEmbed.add_field(name = "Howdy! Call me...", value = "```{}```".format(userGoBy), inline = True)

            if userTimezone != None:
                profileEmbed.add_field(name = "My timezone is...", value = "```{}```".format(userTimezone), inline = True)

            if userIntFacts != None:
                profileEmbed.add_field(name = "Here is an interesting fact about me!", value = "```{}```".format(userIntFacts), inline = True)

            event.msg.reply(embed = profileEmbed)

        else:
            event.msg.reply("This user does not have a profile! Maybe they should make one by changing their settings :eyes:")


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

