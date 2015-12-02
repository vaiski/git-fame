# -*- coding: utf-8 -*-

import click

import re
import subprocess
import datetime
from matplotlib import pyplot as plt
from pprint import pprint


@click.group()
def main():
    pass


def rgb(r, g, b):
    D = 256.0
    return (r/D, g/D, b/D)

COLORS = [
    rgb(241, 106, 0),
    rgb(221,  142, 2),
    rgb(250, 245, 51),
    rgb(155, 227, 25),
    rgb(71, 182, 59),
    rgb(35, 133, 133),
    rgb(18, 79, 213),
    rgb(61, 54, 143),
    rgb(71, 28, 97),
    rgb(116, 28, 84),
    rgb(198, 0, 60),
    rgb(230, 54, 0),
]


@click.command()
@click.option('--since', type=unicode)
@click.option('--until', type=unicode)
def commits(since=None, until=None):
    title = "Commits by Author"
    args = ['git', 'shortlog', '-sn']

    if since is not None:
        args.append('--since=' + since)
        title = title + " From " + since

    if until is not None:
        args.append('--until=' + until)
        title = title + " Until " + until
    else:
        title = title + " Until " + datetime.date.today().isoformat()

    sub = subprocess.Popen(args, stdout=subprocess.PIPE, close_fds=True)

    labels = []
    values = []
    # colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']

    for line in sub.stdout:
        commits, name = [term.strip() for term in line.split('\t')]
        labels.append(name.split()[0])
        values.append(commits)

    plt.axis("equal")
    plt.title(title)
    plt.pie(values, labels=labels, colors=COLORS, autopct='%1.1f%%', labeldistance=1.1)
    plt.savefig('commits.pdf', bbox_inches='tight')

main.add_command(commits)


@click.command()
@click.option('--since', type=unicode)
@click.option('--until', type=unicode)
def changes(since=None, until=None):
    title = "Changes by Author"
    args = ['git log --no-merges --shortstat --pretty=format:"%at %aN"']

    if since is not None:
        args[0] += ' --since="' + since + '"'
        title = title + " From " + since

    if until is not None:
        args[0] += ' --until="' + until + '"'
        title = title + " Until " + until
    else:
        title = title + " Until " + datetime.date.today().isoformat()

    sub = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
    data = {}
    author = ''

    for line in sub.stdout:
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
    labels = [l.split()[0] for l in data.keys()]

    plt.axis("equal")
    plt.title(title)
    plt.pie(values, labels=labels, colors=COLORS, autopct='%1.1f%%', labeldistance=1.1)
    plt.savefig('changes.pdf', bbox_inches='tight')

main.add_command(changes)
