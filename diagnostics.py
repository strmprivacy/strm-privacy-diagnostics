import argparse

from metrics import *


def main(args: dict):
    df = pd.read_csv(args['file'], on_bad_lines='skip', lineterminator='\n')

    if args['sample'] > 0:
        df = df.sample(n=int(args['sample']), random_state=0).reset_index(drop=True)
    df['indexed_row'] = df.index.values
    qi = args['qi']
    sa = args['sa']
    calculate_stats(df, qi, sa)
    return 0


def calculate_stats(df: pd.DataFrame, qi: list, sa: list):
    k = k_anonymity(df, qi)
    l = l_diversity(df, qi, sa)

    # k-Anonymity
    print(f'Your data has a k-Anonymity of: {min(k)}, with {sum(min(k) == k)} occurence(s)')
    print('The 5 smallest equivalence groups with number of occurences are:')
    [print(f'k:{x},n:{sum(x == k)}', end='  ') for x in sorted(np.unique(k))[:5]]

    print('')

    # l-Diversity
    print('Minimal distinct values per equivalence group:')
    [print(f'{k}: {v}', end=',  ') for k, v in l.items()]

    print('')

    # t-Closeness
    t = t_closeness(df, qi, sa)
    print(f"Your data has a t-closeness of: {t:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, help='path to data file')
    parser.add_argument('--qi', nargs='+', help='names of the quasi identifier columns')
    parser.add_argument('--sa', nargs='+', help='names of the sensitive value columns')
    parser.add_argument('--sample', type=int, help='random sample size', default=0)
    arguments = vars(parser.parse_args())
    main(arguments)
