from pareto import Pareto, get_paretos
from plots import plot_pareto, scatter_3d, pairplot
from refactoring import get_ref_actions, ref_actions_stats, reduce_map_to_solutions

import pandas as pd

FIGS = '../figs/'
OUTPUT_DIR = '../data/analysis_results'


def get_initial(reliability):
    return pd.DataFrame([[0, reliability, 0]],
                        columns=['perfQ', 'reliability', '#changes'])
