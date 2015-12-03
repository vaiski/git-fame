# -*- coding: utf-8 -*-

import click
import re
import datetime
import numpy as np
from matplotlib import pyplot as plt
from .utils import git_log, time_title
from .charts import heatmap, changebars, pie


@click.group()
def main():
    pass


@click.command()
@click.option('--since', type=unicode)
@click.option('--until', type=unicode)
def commits(**kwargs):
    '''
    Create a pie chart on commits by author.
    '''
    title = time_title("Commits by Author", **kwargs)
    labels = []
    values = []

    output = git_log('sn', logcmd='shortlog', **kwargs)

    for line in output:
        commits, name = [term.strip() for term in line.split('\t')]
        labels.append(name.split()[0])
        values.append(commits)

    pie(labels, values, title=title)
    plt.savefig('commits.png', bbox_inches='tight')

main.add_command(commits)


@click.command()
@click.option('--since', type=unicode)
@click.option('--until', type=unicode)
def changes(**kwargs):
    '''
    Create a pie chart on total changes and a bar chart on insertions and
    deletions by author.
    '''
    title = time_title("Changes by Author", **kwargs)

    kwargs.update({'pretty': 'format:%at %aN'})
    output = git_log('-no-merges', '-shortstat', **kwargs)

    data = {}
    author = ''

    for line in output:
        line = line.rstrip('\n')
        if len(line) > 0:
            if re.search('files? changed', line) is None:
                sep = line.find(' ')
                # timestamp = line[:sep]
                name = line[sep+1:]
                author = name

                if name not in data.keys():
                    data[name] = {'files': 0, 'inserts': 0, 'deletes': 0, 'total': 0}
            else:
                numbers = re.findall('\d+', line)

                data[author]['files'] += int(numbers[0])

                if len(numbers) == 2:
                    data[author]['total'] += int(numbers[1])

                    if line.find('(+)') != -1:
                        data[author]['inserts'] += int(numbers[1])
                    elif line.find('(-)') != -1:
                        data[author]['deletes'] += int(numbers[1])
                else:
                    data[author]['inserts'] += int(numbers[1])
                    data[author]['deletes'] += int(numbers[2])
                    data[author]['total'] += int(numbers[1]) + int(numbers[2])

    values = [d['total'] for _, d in data.iteritems()]
    deletes = [-1*d['deletes'] for _, d in data.iteritems()]
    inserts = [d['inserts'] for _, d in data.iteritems()]
    labels = [l.split()[0] for l in data.keys()]

    pie(labels, values, title=title)
    plt.savefig('changes.png', bbox_inches='tight')

    changebars(labels, inserts, deletes)
    plt.savefig('changes_bar.png', bbox_inches='tight')

main.add_command(changes)


@click.command()
@click.option('--author', type=unicode, help='Include commits only by given author.')
def activity(**kwargs):
    '''
    Generate a heatmap on repository activity.
    '''
    wdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    weeks = range(52)
    data = {}

    kwargs.update({
        'pretty': 'format:%at',
        'since': datetime.date.today().replace(month=1, day=1)
    })
    output = git_log('-no-merges', **kwargs)

    for line in output:
        timestamp = line.strip('\n')
        if timestamp not in data:
            data[timestamp] = 0
        data[timestamp] += 1

    values = np.zeros([len(wdays), len(weeks)])

    for timestamp, value in data.iteritems():
        date = datetime.date.fromtimestamp(int(timestamp)).isocalendar()
        weekday = date[2] - 1
        week = date[1] - 1

        values[weekday][week] += value

    heatmap(values, weeks, wdays)
    plt.savefig('activity.png', bbox_inches='tight')

main.add_command(activity)
