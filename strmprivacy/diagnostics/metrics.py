import collections
import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_string_dtype


def k_anonymity(df: pd.DataFrame, qi: list[str]) -> pd.Series:
    return df[qi].value_counts()


def l_diversity(df: pd.DataFrame, qi: list[str], sa: list[str]) -> dict[str, list[str]]:
    df_grouped = df.groupby(qi, as_index=False)
    return {s: sorted([len(row['unique']) for _, row in df_grouped[s].agg(['unique']).iterrows()]) for s in sa}


def t_closeness_cat(m: int, r: np.array) -> float:
    return np.sum([np.abs(r[i]) for i in range(m)]) / 2


def t_closeness_num(m: int, r: np.array) -> float:
    emd = np.sum(np.abs(np.cumsum(r[:m])))
    return 1 / (m - 1) * emd


def t_closeness(df: pd.DataFrame, qi: list[str], sa: list[str], sa_types: list[str]) -> float:
    emd_max = 0
    equivalence_classes = [np.array(group['indexed_row']) for _, group in df.groupby(qi)]
    for i, s in enumerate(sa):
        values = sorted(df[s].unique())
        m = len(values)
        p = collections.defaultdict(float, dict(df[s].value_counts() / len(df)))
        p = [p[x] for x in values]
        for ec in equivalence_classes:
            df_ec = df.iloc[ec]
            qis = collections.defaultdict(float, dict(df_ec[s].value_counts() / len(ec)))
            r = np.array([qis[x] - p[j] for j, x in enumerate(values)])
            if len(sa_types) > 0:
                if sa_types[i] == "cat":
                    emd_max = max(emd_max, t_closeness_cat(m, r))
                elif sa_types[i] == "num":
                    emd_max = max(emd_max, t_closeness_num(m, r))
            elif is_string_dtype(df[s]):
                emd_max = max(emd_max, t_closeness_cat(m, r))
            elif is_numeric_dtype(df[s]):
                emd_max = max(emd_max, t_closeness_num(m, r))
    return emd_max
