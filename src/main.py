import os
from subprocess import call

cToRun = "python3.6 -m disco.cli --config config.json"
call(cToRun, shell = True)
