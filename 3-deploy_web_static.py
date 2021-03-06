#!/usr/bin/python3
"""Packs web_static into a tgz archive using Fabric"""
from fabric.api import *
import os
from datetime import datetime

env.hosts = ['35.196.185.161', '104.196.150.129']


@runs_once
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


def do_deploy(archive_path):
    """Uploads archive at archive_path to remote servers, unpacks archive and
    creates a symbolic link"""
    if not os.path.isfile(archive_path):
        return False

    filename = archive_path.split('/')[-1]
    tmp_arc_path = "/tmp/" + filename
    data_arc_path = "/data/web_static/releases/{}"\
        .format(filename.split('.')[0])

    put(archive_path, tmp_arc_path)
    commands = ["mkdir -p {}/".format(data_arc_path),
                "tar -xzf {} -C {}/".format(tmp_arc_path, data_arc_path),
                "rm " + tmp_arc_path,
                "mv {}/web_static/* {}/".format(data_arc_path, data_arc_path),
                "rm -rf {}/web_static".format(data_arc_path),
                "rm -rf /data/web_static/current",
                "ln -s {}/ /data/web_static/current".format(data_arc_path)
                ]

    for command in commands:
        r = run(command)
        if r.failed:
            return False

    print("New version deployed!")

    return True


def deploy():
    """Performs do_pack() and do_deploy(archive_path)"""
    path = do_pack()
    if path is None and arc_path is None:
        return False
    if path is not None:
        arc_path = path

    return do_deploy(arc_path)
