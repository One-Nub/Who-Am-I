# Who Am I

__Who Am I__ is a discord bot meant to make sharing info about yourself easier to those in your servers!

# Invite me!
[Invite URL](https://discordapp.com/oauth2/authorize?client_id=592796597209792542&permissions=380096&scope=bot)

The default prefix is `wai!` or you can mention the bot.

## Installation

All configuration values will be found in [config.json](https://github.com/One-Nub/Who-Am-I/blob/master/src/config.json) allowing the self hoster (you!) to just configure those values & away you go. (Although my name and github links will still be hidden in places :eyes:)

The MariaDB user requires CREATE, INSERT, SELECT, and UPDATE.

Run the bot with `python -m disco-cli --config config.json` from the `/src` directory. 
`/src/main.py` can be used as well but this will not work if a virtual environment is set - or if python is not named python3.6.

## Requirements

This requires at least [Python3.6+](https://www.python.org/downloads/) to be able to run as well as a [MariaDB](https://mariadb.org/) database.
The MariaDB user requires CREATE, INSERT, SELECT, and UPDATE permissions.

```bash
pip3 install -r requirements.txt

#OR RUN
pip3 install git+git://github.com/b1naryth1ef/disco#egg=disco-py
pip3 install mysql-connector-python~=8.0.16  
```

## Post Hackweek Ideas
- Add server join date to the profile
- Add account creation date to the profile
- Add further fields to the profile (such as what games they play, etc..)

## License
[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
