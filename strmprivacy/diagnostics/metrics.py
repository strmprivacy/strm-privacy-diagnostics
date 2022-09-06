import collections
import pandas as pd
import numpy as np
from scipy.stats import wasserstein_distance as wd


def k_anonymity(df: pd.DataFrame, qi: list[str]) -> pd.Series:
    return df[qi].value_counts()


def l_diversity(df: pd.DataFrame, qi: list[str], sa: list[str]) -> dict[str, list[str]]:
    df_grouped = df.groupby(qi, as_index=False)
    return {s: sorted([len(row['unique']) for _, row in df_grouped[s].agg(['unique']).iterrows()]) for s in sa}


def t_closeness_cat(df: pd.DataFrame, qi: list[str], s: str) -> float:
    emd_max = 0
    equivalence_classes = [np.array(group['indexed_row']) for _, group in df.groupby(qi)]
    values = sorted(df[s].unique())
    m = len(values)
    p = collections.defaultdict(float, dict(df[s].value_counts() / len(df)))
    p = [p[x] for x in values]
    for ec in equivalence_classes:
        df_ec = df.iloc[ec]
        qis = collections.defaultdict(float, dict(df_ec[s].value_counts() / len(ec)))
        r = np.array([qis[x] - p[j] for j, x in enumerate(values)])
        emd_max = max(emd_max, np.sum([np.abs(r[i]) for i in range(m)]) / 2)
    return emd_max


def t_closeness_num(df: pd.DataFrame, qi: list[str], s: str) -> float:
    emd_max = 0
    equivalence_classes = [np.array(group['indexed_row']) for _, group in df.groupby(qi)]
    values = df[s]
    max_distance = max(values) - min(values)
    for ec in equivalence_classes:
        q_values = df.iloc[ec][s]
        emd_max = max(emd_max, wd(values, q_values) / max_distance)
    return emd_max


def t_closeness(df: pd.DataFrame, qi: list[str], sa: list[str], sa_types: list[str]) -> float:
    emd_max = 0
    for i, s in enumerate(sa):
        if sa_types[i] == "cat":
            emd_max = max(emd_max, t_closeness_cat(df, qi, s))
        elif sa_types[i] == "num":
            emd_max = max(emd_max, t_closeness_num(df, qi, s))
    return emd_max
