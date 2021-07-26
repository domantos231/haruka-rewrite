import configparser
import os
import platform
import shutil
import subprocess
from lib.settings import *


cur.execute("SELECT * FROM queue;")
lst = cur.fetchall()
config = configparser.ConfigParser()
config["general"] = {"status": "ready"}
for obj in lst:
    id = obj[0]
    queue = [url for url in obj[1] if url is not None]
    try:
        shutil.rmtree(f"{root}/music/{id}-music")
    except:
        pass
    finally:
        os.mkdir(f"{root}/music/{id}-music")
        os.chdir(f"{root}/music/{id}-music")
        with open("config.ini", "w") as inifile:
            config.write(inifile)
        for link in enumerate(queue):
            while not os.path.isfile(f"song{link[0] + 1}.opus"):
                if platform.system() == "Windows":
                    subprocess.call(f"youtube-dl --no-playlist --extract-audio --audio-format \"opus\" --match-filter \"!is_live\" --force-ipv4 --rm-cache-dir -o \"song{link[0] + 1}.%(ext)s\" {link[1]}", shell = True)
                else:
                    subprocess.call(f"youtube-dl --no-playlist --extract-audio --audio-format 'opus' --match-filter '!is_live' --force-ipv4 --rm-cache-dir -o 'song{link[0] + 1}.%(ext)s' {link[1]}", shell = True)
