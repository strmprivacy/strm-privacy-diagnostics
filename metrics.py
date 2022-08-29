import collections

import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_string_dtype


def k_anonymity(df: pd.DataFrame, qi: list) -> list:
    return df[qi].value_counts().values


def l_diversity(df: pd.DataFrame, qi: list, s: list) -> dict:
    df_grouped = df.groupby(qi, as_index=False)
    return {col: min([len(row['unique']) for _, row in df_grouped[col].agg(['unique']).iterrows()]) for col in s}


def t_closeness_cat(m: int, r: np.array) -> float:
    return sum([np.abs(r[i]) for i in range(m)]) / 2


def t_closeness_num(m: int, r: np.array) -> float:
    emd = sum(np.abs(np.cumsum(r[:m])))
    return 1 / (m - 1) * emd


def t_closeness(df: pd.DataFrame, qi: list, sa: list) -> float:
    emd_max = 0
    for s in sa:
        equivalence_classes = [np.array(group['indexed_row']) for _, group in df.groupby(qi)]
        values = sorted(df[s].unique())
        m = len(values)
        p = collections.defaultdict(float, dict(df[s].value_counts() / len(df)))
        p = np.array([p[x] for x in values])

        for ec in equivalence_classes:
            df_ec = df.iloc[ec]
            qis = collections.defaultdict(float, dict(df_ec[s].value_counts() / len(ec)))
            qis = np.array([qis[x] for x in values])
            r = qis - p
            if is_string_dtype(df[s]):
                emd_max = max(emd_max, t_closeness_cat(m, r))
            elif is_numeric_dtype(df[s]):
                emd_max = max(emd_max, t_closeness_num(m, r))
    return emd_max
