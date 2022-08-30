import argparse
import logging
import tempfile

from metrics import *
from strm_privacy_diagnostics.src.report.report import Report
from strm_privacy_diagnostics.src.plots import plot_l_diversity, plot_k_anonymity


def main(args: dict):
    qi = args['qi']
    sa = args['sa']
    sa_types = args['sa_types']
    metrics = args['metrics']

    assert_arguments(qi, sa, sa_types)

    df = pd.read_csv(args['file'], on_bad_lines='warn')
    if 0 < args['sample'] <= len(df):
        df = df.sample(n=int(args['sample']), random_state=0).reset_index(drop=True)
    df['indexed_row'] = df.index.values
    assert_columns(df, qi + sa)
    calculate_stats(df, qi, sa, sa_types, metrics, args['report_path'])


def assert_arguments(qi: list[str], sa: list[str], sa_types: list[str]):
    if len(sa_types) > 0:
        assert len(sa_types) == len(sa), "Length of sa-types doesn't equal length of sa. " \
                                         "Either leave empty or set all data types explicitly."
        assert all(x in ["cat", "num"] for x in sa_types), "Wrong type given for sensitive attribute." \
                                                           "Valid types: [cat, num]"
    else:
        logging.warning("No sensitive attribute type was defined. Types will be inferred.")
    assert len(qi), "No quasi identifiers were defined. Please define at least one quasi identifier."
    assert len(sa), "No sensitive attributes were defined. Please define at least one sensitive attributes."
    assert not any(x in qi for x in sa), "A quasi identifier cannot also be a sensitive attribute."


def assert_columns(df: pd.DataFrame, columns: list[str]):
    for column in columns:
        assert column in df.columns, f"Column {column} does not exist in the given dataset"


def calculate_stats(df: pd.DataFrame, qi: list[str], sa: list[str], sa_types: list[str], metrics: list[str], path: str):
    # k-Anonymity
    k = k_anonymity(df, qi) if 'k_anonymity' in metrics else None
    # l-Diversity
    l = l_diversity(df, qi, sa) if 'l_diversity' in metrics else None
    # t-Closeness
    t = t_closeness(df, qi, sa, sa_types) if 't_closeness' in metrics else None

    with tempfile.TemporaryDirectory() as tmpdir:
        # Plots
        if k is not None:
            plot_k_anonymity(df, k, tmpdir)
        if l is not None:
            plot_l_diversity(df, sa, l, tmpdir)

        # Report
        Report(tmpdir=tmpdir).create(k, l, t, path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, help='path to data file')
    parser.add_argument('--qi', nargs='+', help='names of the quasi identifier columns', default=[])
    parser.add_argument('--sa', nargs='+', help='names of the sensitive attribute columns', default=[])
    parser.add_argument('--sa-types', nargs='+', help='data types of the sensitive attribute columns. '
                                                      'valid types: [cat, num]', default=[])
    parser.add_argument('--metrics', nargs='+', help='pick the metric you want in your report',
                        default=['k_anonymity', 'l_diversity', 't_closeness'])
    parser.add_argument('--sample', type=int, help='random sample size', default=0)
    parser.add_argument('--report-path', type=str, help='path to save report to', default='.')
    arguments = vars(parser.parse_args())
    main(arguments)
