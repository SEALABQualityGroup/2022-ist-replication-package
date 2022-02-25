import re
from glob import glob
from os.path import basename

import pandas as pd

DATA_DIR = '../data/'
REF_ACTIONS = DATA_DIR + 'refactoring_actions/'
OBJECTIVES = DATA_DIR + 'objectives/'
QI = DATA_DIR + 'quality_indicators/qi.csv'


class RefActions:

    def __init__(self, files):
        self.files = files
        self.parse_filenames()

    def parse_filenames(self):
        m = re.match(r'VAR\d+__(?P<usecase>[^_]+)__BRF_clone_(?P<brf_clone>[^_]+)__moc_(?P<brf_moc>[^_]+)__mcnn_(?P<brf_mcnn>[^_]+)__moncnn_(?P<brf_moncnn>[^_]+)__MaxEval_(?P<maxeval>[^_]+)__ProbPAs_(?P<probpas>[^_]+)\.csv', basename(self.files[0]))
        if m is not None:
            for k, v in m.groupdict().items():
                setattr(self, k, v)
            self.config = m.groupdict().keys()
        else:
            print('Cannot parse:', self.files[0])

    def extract_ref_actions(self):
        return pd.concat([pd.read_csv(f) for f in self.files])

def query_ref_actions(query):
    # put runs together
    ref_actions = [RefActions(glob(f.replace('VAR0', 'VAR[0-9]')))
            for f in glob(REF_ACTIONS + 'VAR0__*.csv')]

    selected = []
    for act in ref_actions:
        for k, v in query.items():
            if getattr(act, k) != v:
                break
        else:
            selected.append(act)

    return selected

def get_ref_actions(query):
    selected = query_ref_actions(query)
    return pd.concat([exp.extract_ref_actions() for exp in selected])

def ref_actions_stats(query):
    actions = get_ref_actions(query)
    return actions['operation'].value_counts(normalize=True)\
            .apply(lambda x:x*100)

def reduce_map_to_solutions(query):
    actions = query_ref_actions(query)
    mapped = []
    for act in actions:
        for f in act.files:
            # read the refactoring actions from the VAR files
            df = pd.read_csv(f)

            # reduce (4 rows to 1 row containing only the counts)
            rds = []
            for i in range(0, df.shape[0], 4):
                types = df[i:i+4]['operation'].value_counts()
                ops = df[i:i+4]['operation']
                ops.index = ['action{}'.format(i) for i in range(1, 5)]
                targets = df[i:i+4]['target']
                targets.index = ['target{}'.format(i) for i in range(1, 5)]
                rds.append(pd.concat([types, ops, targets]))
            rd = pd.DataFrame(rds)
            #rd = pd.DataFrame([df[i:i+4]['operation'].value_counts()
            #    for i in range(0, df.shape[0], 4)])
            #rd.reset_index(drop=True, inplace=True)

            # read the objectives from the FUN files
            obj = pd.read_csv(OBJECTIVES + basename(f).replace('VAR', 'FUN'))
            obj['perfQ'] = obj['perfQ'] * -1
            obj['reliability'] = obj['reliability'] * -1

            # add information about the experiment
            for k in act.config:
                obj[k] = getattr(act, k)

            # read the quality indicators
            qi = pd.read_csv(QI)

            # map
            mp = pd.concat([obj, rd], axis=1)
            mapped.append(mp)

    mapped_df = pd.concat(mapped)
    mapped_df.reset_index(drop=True, inplace=True)
    mapped_df = mapped_df.fillna(0)
    return mapped_df
