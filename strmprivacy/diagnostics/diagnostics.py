import argparse
import logging
import tempfile

from pandas.core.dtypes.common import is_string_dtype, is_numeric_dtype

from strmprivacy.diagnostics.metrics import *
from strmprivacy.diagnostics.report.report import Report
from strmprivacy.diagnostics.plots import plot_l_diversity, plot_k_anonymity


class PrivacyDiagnostics:
    defaultMetrics = ['k_anonymity', 'l_diversity']

    def __init__(self, file: str, sample: int = 0):
        self.k, self.l, self.t = None, None, None
        self.file = file
        self.df = pd.read_csv(file, on_bad_lines='warn')
        if 0 < sample <= len(self.df):
            self.df = self.df.sample(n=int(sample), random_state=0).reset_index(drop=True)
        self.df['indexed_row'] = self.df.index.values

    def calculate_stats(self, qi: list[str], sa: list[str] = [], sa_types=[],
                        metrics=defaultMetrics):
        self.assert_arguments(qi, sa, sa_types, metrics)
        self.assert_columns(qi + sa)

        if len(sa_types) == 0:
            for s in sa:
                if is_string_dtype(self.df[s]):
                    sa_types.append('cat')
                elif is_numeric_dtype(self.df[s]):
                    sa_types.append('num')
                else:
                    raise TypeError(f"Cannot infer type of column '{s}'")
        # k-Anonymity
        self.k = k_anonymity(self.df, qi) if 'k_anonymity' in metrics else None
        # l-Diversity
        self.l = l_diversity(self.df, qi, sa) if 'l_diversity' in metrics and len(sa) > 0 else None
        # t-Closeness
        self.t = t_closeness(self.df, qi, sa, sa_types) if 't_closeness' in metrics and len(sa) > 0 else None

    def create_report(self, qi: list[str], sa: list[str] = [], sa_types: list[str] = [],
                      metrics=defaultMetrics, path: str = '.'):
        if ('k_anomyity' in metrics and self.k is None) or \
                ('l_diversity' in metrics and self.l is None) or \
                ('t_closeness' in metrics and self.t is None):
            self.calculate_stats(qi, sa, sa_types, metrics)

        with tempfile.TemporaryDirectory() as tmpdir:
            # Plots
            if self.k is not None:
                plot_k_anonymity(self.df, self.k, tmpdir)
            if self.l is not None:
                plot_l_diversity(self.df, sa, self.l, tmpdir)

            # Report
            Report(tmpdir=tmpdir).create(self.k, self.l, self.t, path)

    def assert_columns(self, columns: list[str]):
        for column in columns:
            assert column in self.df.columns, f"Column '{column}' does not exist in the given dataset"

    @staticmethod
    def assert_arguments(qi: list[str], sa: list[str], sa_types: list[str] = [],
                         metrics: list[str] = defaultMetrics):
        if len(sa_types) > 0:
            assert len(sa_types) == len(sa), "Length of sa-types doesn't equal length of sa. " \
                                             "Either leave empty or set all data types explicitly."
            assert all(x in ["cat", "num"] for x in sa_types), "Wrong type given for sensitive attribute. " \
                                                               "Valid types: [cat, num]"
        else:
            logging.warning("No sensitive attribute type was defined. Types will be inferred.")
        assert len(qi), "No quasi identifiers were defined. Please define at least one quasi identifier."
        if len(sa) == 0:
            logging.warning("No sensitive attributes were defined. Only k-anonymity can be calculated.")
        assert not any(x in qi for x in sa), "A quasi identifier cannot also be a sensitive attribute."
        assert all(m in ['k_anonymity', 'l_diversity', 't_closeness'] for m in metrics), \
            "Unknown metrics specified. Valid types: [k_anonymity, l_diversity, t_closeness]"
        if 't_closeness' in metrics:
            logging.warning("t-Closeness can drastically increase calculation times with larger datasets and number "
                            "of sensitive attributes.")


def main(args: dict):
    file, qi, sa, sa_types, sample, report_path, metrics = args['file'], args['qi'], args['sa'], args['sa_types'], args[
        'sample'], args['report_path'], args['metrics']
    diagnostics = PrivacyDiagnostics(file, sample)
    diagnostics.assert_arguments(qi, sa, sa_types, metrics)
    diagnostics.create_report(qi, sa, sa_types, metrics, report_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, help='path to data file')
    parser.add_argument('--qi', nargs='+', help='names of the quasi identifier columns', default=[])
    parser.add_argument('--sa', nargs='+', help='names of the sensitive attribute columns', default=[])
    parser.add_argument('--sa-types', nargs='+', help='data types of the sensitive attribute columns. '
                                                      'valid types: [cat, num]', default=[])
    parser.add_argument('--metrics', nargs='+', help='pick the metric you want in your report',
                        default=['k_anonymity', 'l_diversity'])
    parser.add_argument('--sample', type=int, help='random sample size', default=0)
    parser.add_argument('--report-path', type=str, help='path to save report to', default='.')
    arguments = vars(parser.parse_args())
    main(arguments)
