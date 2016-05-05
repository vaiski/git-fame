# -*- coding: utf-8 -*-

import re
import numpy as np
import pandas as pd

from gitfame.utils import git_log


def commitcount(**kwargs):
    print kwargs
    output = git_log('sn', logcmd='shortlog', **kwargs)

    values = []
    for line in output:
        commits, name = [term.strip() for term in line.split('\t')]
        values.append((name.split()[0], commits))

    return pd.DataFrame(values,
                        columns=['author', 'commits'])


def changecount(**kwargs):
    kwargs.update({'pretty': 'format:%at %aN'})
    output = git_log('-no-merges', '-shortstat', **kwargs)

    timestamp = ''
    author = ''
    values = []

    for line in output:
        line = line.rstrip('\n')

        if len(line) > 0:
            if re.search('files? changed', line) is None:
                sep = line.find(' ')
                timestamp = int(line[:sep])
                author = line[sep:].split()[0]

            else:
                values.append(processRow(timestamp, author, line))

    return pd.DataFrame(values,
                        columns=['timestamp', 'author', 'inserts', 'deletes', 'changes'])


def processRow(timestamp, author, line):
    numbers = re.findall('\d+', line)
    timestamp = pd.to_datetime(timestamp, unit='s')
    if len(numbers) == 2:
        if line.find('(+)') != -1:
            return (timestamp, author, int(numbers[1]), 0, int(numbers[1]))
        elif line.find('(-)') != -1:
            return (timestamp, author, 0, int(numbers[1]), int(numbers[1]))

    return (timestamp, author, int(numbers[1]), int(numbers[2]), int(numbers[1]) + int(numbers[2]))
