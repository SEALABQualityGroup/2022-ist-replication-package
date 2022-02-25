import re
from glob import glob
from os.path import basename

import pandas as pd

DATA_DIR = '../data/'
REF_PARETOS = DATA_DIR + 'reference_paretos/'

class Pareto:

    def __init__(self, file):
        self.file = file
        self.parse_filename()
        self.read_rf()

    def parse_filename(self):
        m = re.match(r'(?P<usecase>[^_]+)__BRF_clone_(?P<brf_clone>[^_]+)__moc_(?P<brf_moc>[^_]+)__mcnn_(?P<brf_mcnn>[^_]+)__moncnn_(?P<brf_moncnn>[^_]+)__MaxEval_(?P<maxeval>[^_]+)__ProbPAs_(?P<probpas>[^_]+)__Algo_(?P<algo>[^_]+)\.rf', basename(self.file))
        if m is not None:
            for k, v in m.groupdict().items():
                setattr(self, k, v)

    def read_rf(self):
        with open(self.file) as f:
            first_line = f.readline()
        sep = r'\s+'
        if ',' in first_line:
            sep=','
        df = pd.read_csv(self.file, sep=sep, index_col='solID')
        if df.columns[-1].startswith('Unnamed:'):
            df = df.drop(df.columns[-1], axis=1)
        self.df = Pareto.fix_perfq_rel(df)
        return self.df

    @staticmethod
    def fix_perfq_rel(df):
        if 'perfQ' in df:
            df['perfQ'] = df['perfQ'] * -1
        if 'reliability' in df:
            df['reliability'] = df['reliability'] * -1
        return df


def get_paretos(query):
    rfs = [Pareto(rf) for rf in glob(REF_PARETOS + '*.rf')]
    result = []
    for rf in rfs:
        if rf.df.shape[0] == 0:
            print('Empty file:', rf.file)
            continue
        for k, v in query.items():
            if not hasattr(rf, k) or getattr(rf, k) != v:
                break
        else:
            result.append(rf)
    return result
