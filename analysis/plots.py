import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
import pandas as pd
import numpy as np

def sol_scatter(ax, df, marker, markersize, color, label=''):
    return ax.scatter(df['perfQ'], df['reliability'],
            s=df['#changes']*markersize, marker=marker, label=label,
            alpha=0.5, c=color)

def labels(ax, artists, hue):
    ax.set_xlabel('PerfQ', fontsize=20)
    ax.set_ylabel('Reliability', fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=16)
    #lgnd = plt.legend(loc='lower right', handletextpad=-0.3, fontsize=16)
    fake = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
    lgnd = plt.legend([fake] + artists,
            [hue] + [a.get_label() for a in artists],
            loc='upper center', handletextpad=-0.3, fontsize=16,
            fancybox=True, shadow=False, ncol=len(artists)+1, bbox_to_anchor=(0.5, 1.1))
    for handle in lgnd.legendHandles[1:]:
        handle.set_sizes([50])

def plot_initial(ax, sol):
    ax.scatter(sol['perfQ'], sol['reliability'], s=75, marker='X', alpha=1, c='black')
    ax.annotate("initial", fontsize=14, xy=(sol['perfQ'], sol['reliability']), xycoords='data',
                xytext=(25, -25), textcoords='offset points', ha="left", va="center",
                arrowprops=dict(arrowstyle="wedge,tail_width=.01", facecolor='black'))

def plot_pareto(experiments, hue, initial=None, save_prefix=None,
        colors=[7, 0, 2, 3], markers=['s', 'o', '^', 'D', 'p'],
        legend_title=None):
    experiments.sort(key=lambda x: getattr(x, hue))

    fig, ax = plt.subplots(figsize=[10, 8])

    # Plot
    artists = []
    for i, exp in enumerate(experiments):
        ax.set_ylim([0, 1])
        #ax.set_xlim([-0.07, 0.27])
        artists.append(sol_scatter(ax, exp.read_rf(), markers[i], 50,
            color=[plt.cm.tab10(colors[i])], label=getattr(exp, hue)))

    # Initial solution
    if initial is not None:
        plot_initial(ax, initial)

    # Labels
    if legend_title is None:
        legend_title = hue
    labels(ax, artists, legend_title)

    # Grid
    ax.set_axisbelow(True)
    ax.xaxis.grid(color='gray', linestyle='dashed')
    ax.yaxis.grid(color='gray', linestyle='dashed')

    plt.tight_layout()

    filename = '{}_2dscatter.pdf'.format(save_prefix)
    plt.savefig(filename)
    print('Saved to: {}'.format(filename))

def scatter_3d(paretos, hue, save_prefix=None):
    paretos.sort(key=lambda x: getattr(x, hue))
    fig, ax = plt.subplots(figsize=(8, 6))
    ax = fig.add_subplot(projection='3d')
    colors = sns.color_palette('cubehelix', len(paretos))

    for i, p in enumerate(paretos):
        ax.scatter(p.df['perfQ'], p.df['reliability'], p.df['#changes'],
                c=np.array([colors[i]]), label=getattr(p, hue))

    ax.set_xlabel('perfQ')
    ax.set_ylabel('reliability')
    ax.set_zlabel('#changes')
    ax.view_init(45, 45)
    ax.legend(title=hue)

    filename = '{}_3dscatter.pdf'.format(save_prefix)
    plt.savefig(filename)
    print('Saved to: {}'.format(filename))

def pairplot(paretos, hue, save_prefix=None):
    paretos.sort(key=lambda x: getattr(x, hue))
    for p in paretos:
        p.df[hue] = getattr(p, hue)
    df = pd.concat([p.df for p in paretos], ignore_index=True)

    g = sns.pairplot(df, hue=hue, palette='cubehelix')

    incl = ['usecase', 'brf_moc'] +\
        [k for k in ['maxeval', 'probpas'] if k != hue]
    g.fig.subplots_adjust(top=0.9)
    g.fig.suptitle(', '.join(['{}: {}'.format(k, v)
        for k, v in paretos[0].__dict__.items() if k in incl]))

    filename = '{}_pairplot.pdf'.format(save_prefix)
    plt.savefig(filename)
    print('Saved to: {}'.format(filename))

def kde(paretos, hue, save_prefix=None):
    paretos.sort(key=lambda x: getattr(x, hue))
    for p in paretos:
        p.df[hue] = getattr(p, hue)
    df = pd.concat([p.df for p in paretos], ignore_index=True)

    for obj in [c for c in df.columns if c != hue]:
        fig, ax = plt.subplots(figsize=(5, 4))
        g = sns.kdeplot(x=obj, data=df, hue=hue,
                fill=True, palette='cubehelix', ax=ax)
        g.legend_.set_title('PAs prob.')
        ax.set_xlabel('')
        fig.tight_layout()
        filename = '{}_obj_{}_kde.pdf'.format(save_prefix, obj)
        plt.savefig(filename)
        print('Saved to: {}'.format(filename))
        plt.close()
