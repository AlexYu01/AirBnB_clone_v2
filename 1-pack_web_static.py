#!/usr/bin/python3
"""Packs web_static into a tgz archive using Fabric"""
from fabric.api import *
import os
from datetime import datetime


def do_pack():
    """Packs what is inside web_static into a tgz using the name
    `web_static_<year><month><day><hour><minute><second>.tgz`"""

    time = datetime.now()
    created_at = str(time.year) + str(time.month) + str(time.day) +\
        str(time.hour) + str(time.minute) + str(time.second)
    tgz_path = "versions/web_static_{}.tgz".format(created_at)

    command = "tar -cvzf {} web_static".format(tgz_path)

    if not os.path.exists("versions"):
        os.makedirs("versions")
    print("Packing web_static to {}".format(tgz_path))
    result = local(command)
    if result.succeeded:
        return tgz_path
    else:
        return None
