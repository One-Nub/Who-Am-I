# Who Am I

__Who Am I__ is a discord bot meant to make sharing info about yourself easier to those in your servers!

# Invite me!
[Invite URL](https://discordapp.com/oauth2/authorize?client_id=592796597209792542&permissions=380096&scope=bot)

## Installation

All configuration values will be found in [config.json](https://github.com/One-Nub/Who-Am-I/blob/master/src/config.json) allowing the self hoster (you!) to just configure those values & away you go.

The MariaDB user requires CREATE, INSERT, SELECT, and UPDATE.

Run it with main.py in /src

## Requirements

This requires [Python 3.6](https://www.python.org/downloads/release/python-368/) to be able to run as well as a [MariaDB](https://mariadb.org/) database.
The MariaDB user requires CREATE, INSERT, SELECT, and UPDATE.

```bash
sudo pip3 install -r requirements.txt

#OR RUN

sudo pip3 install disco-py==0.0.12
sudo pip3 install mysql-connector-python~=8.0.16  
```

## Post Hackweek Ideas
- Add server join date to the profile
- Add account creation date to the profile
- Add further fields to the profile (such as what games they play, etc..)

## License
[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)