from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
sns.set()


def plot(df: pd.DataFrame, k: list[str], metric: str, tmpdir: str):
    fig = plt.figure(figsize=(12, 8))
    sorted_uniques = list(sorted(np.unique(k)))
    plt.plot([min(sorted_uniques)] + sorted_uniques, [0] + list(np.cumsum([sum(x == k) * x for x in sorted_uniques]) * 100 / len(df)),
             label='unique rows loss')
    plt.plot([min(sorted_uniques)] + sorted_uniques, [0] + list(np.cumsum([sum(x == k) for x in sorted_uniques]) * 100 / len(k)),
             label='unique equivalence group loss')

    fig.suptitle(f'{metric} vs. Data Loss', fontsize=24)
    plt.xlabel(f'{metric} level', fontsize=20)
    plt.ylabel('Percentage data loss', fontsize=20)
    plt.legend(fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlim(left=-10)
    plt.ylim(bottom=-10)
    plt.close(fig)
    fig.savefig(str(Path(tmpdir, f'{metric}.png')))


def plot_k_anonymity(df: pd.DataFrame, k: pd.Series, tmpdir: str):
    plot(df, list(k.values), "k-Anonymity", tmpdir)


def plot_l_diversity(df: pd.DataFrame, sa: list[str], l: dict, tmpdir: str):
    for s in sa:
        plot(df, l[s], f"l-Diversity ({s})", tmpdir)
