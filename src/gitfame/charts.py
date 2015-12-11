# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt

COLORS = plt.cm.YlGn(np.arange(5)/5.)


def heatmap(values, xlabels, ylabels, size=(12, 1.35)):
    fig, ax = plt.subplots()
    plt.axis('equal')
    heatmap = ax.pcolormesh(values, cmap=plt.cm.YlGn)
    plt.colorbar(heatmap, ticks=range(int(values.max().round())+1))
    fig.set_size_inches(*size)

    ax.set_frame_on(False)

    ax.set_xticks(np.arange(values.shape[1])+0.5, minor=False)
    ax.set_yticks(np.arange(values.shape[0])+0.5, minor=False)

    ax.invert_yaxis()
    ax.xaxis.tick_top()
    ax.yaxis.tick_left()
    ax.grid(False)

    ax.set_xticklabels(xlabels, minor=False, size=8)
    ax.set_yticklabels(ylabels, minor=False, size=8)
    for i, label in enumerate(ax.xaxis.get_ticklabels()):
        if i % 5 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)


def pie(labels, values, title=None):
    plt.axis("equal")

    if title is not None:
        plt.title(title)

    plt.pie(values, labels=labels, colors=COLORS, autopct='%1.1f%%', labeldistance=1.1)


def changebars(labels, inserts, deletes):
    plt.axis("tight")
    plt.figure()
    ax = plt.subplot(111)
    ticks = range(len(labels))
    ax.bar(ticks, deletes, width=1, color='crimson')
    ax.bar(ticks, inserts, width=1, color='darkblue')
    plt.xticks([t+0.5 for t in ticks], labels)
