import os
from pareto import get_paretos
from plots import kde

FIGS = '../figs/kde/'

if not os.path.exists(FIGS):
    os.makedirs(FIGS)

for uc in ['train-ticket', 'simplified-cocome-newrel']:
    for brf in ['1.23', '1.64']:
        for maxeval in ['72', '82', '102']:
            rfs = get_paretos(
                    {'brf_moc': brf, 'maxeval': maxeval, 'usecase': uc})
            kde(rfs, 'probpas', save_prefix='{}{}_brf_{}_maxeval_{}'\
                    .format(FIGS, uc, brf, maxeval))
