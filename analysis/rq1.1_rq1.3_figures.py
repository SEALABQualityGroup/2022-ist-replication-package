from pareto import get_paretos
from analysis import get_initial, FIGS
from plots import plot_pareto

case_studies = [
    { 'name': 'train-ticket',
      'shortname': 'ttbs',
      'initial': get_initial(0.657925) },
    { 'name': 'simplified-cocome-newrel',
      'shortname': 'cocome-newrel',
      'initial': get_initial(0.7630625563279512) },
]
brf = '1.23'
maxeval = '72'
probpas = ['0.00', '0.95']

for uc in case_studies:
    rfs = []
    for pas in probpas:
        rfs += get_paretos({'brf_moc': brf, 'maxeval': maxeval,
            'usecase': uc['name'], 'probpas': pas})
    rfs.sort(key=lambda x: x.probpas)
    plot_pareto(rfs, initial=uc['initial'], hue='probpas',
            save_prefix='{}{}_pas_prob_0-95_{}_{}'\
                    .format(FIGS, uc['shortname'], maxeval, brf),
            colors=[7, 3], markers=['s', 'D'], legend_title='PAs prob.')

for uc in case_studies:
    rfs = get_paretos({'brf_moc': brf, 'maxeval': maxeval,
            'usecase': uc['name']})
    rfs.sort(key=lambda x: x.probpas)
    plot_pareto(rfs, initial=uc['initial'], hue='probpas',
            save_prefix='{}{}_pas_prob_{}_{}'\
                    .format(FIGS, uc['shortname'], maxeval, brf),
            legend_title='PAs prob.')
