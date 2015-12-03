# -*- coding: utf-8 -*-

import datetime
import subprocess


def rgb(r, g, b):
    D = 256.0
    return (r/D, g/D, b/D)


def git_log(*args, **kwargs):
    cmd = ['git', kwargs.get('logcmd', 'log')]

    if 'logcmd' in kwargs:
        del kwargs['logcmd']

    for arg in args:
        cmd.append("-{}".format(arg))

    for key, value in kwargs.iteritems():
        if value is not None:
            cmd.append('--{}="{}"'.format(key, value))

    sub = subprocess.Popen([' '.join(cmd)], stdout=subprocess.PIPE, shell=True)
    return sub.stdout


def time_title(title, since=None, until=None, **kwargs):
    if since is not None:
        title = title + " From " + since

    if until is not None:
        title = title + " Until " + until
    else:
        title = title + " Until " + datetime.date.today().isoformat()

    return title
