import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from refactoring import *

FIGS = '../figs/'

BRF = ['1.23', '1.64']
MAXEVAL = ['72', '82', '102']
PROBPAS = ['0.00', '0.55', '0.80', '0.95']
REF_ACTIONS = {
    'UMLCloneNode': 'Clon',
    'Move_Operation_New_Component_New_Node': 'MO2N',
    'Move_Operation_Component': 'MO2C',
    'Move_Component_New_Node': 'ReDe'
}

def ref_actions_by_configs(usecase):
    actions_df = []
    configs_df = []
    for brf in BRF:
        for maxeval in MAXEVAL:
            for probpas in PROBPAS:
                query = {'usecase': usecase, 'brf_moc': brf, 'maxeval': maxeval,
                        'probpas': probpas}
                actions = ref_actions_stats(query)
                actions_df.append(actions)
                configs_df.append(query)
    query_all = {'usecase': usecase}
    configs_df.append(query_all)
    actions_df.append(ref_actions_stats(query_all))
    configs = pd.DataFrame(configs_df)
    df = pd.DataFrame(actions_df)
    df.reset_index(drop=True, inplace=True)
    df = pd.concat([configs, df[REF_ACTIONS.keys()]], axis=1)
    return df

def print_ref_actions_by_configs(usecase):
    print('Share of refactoring actions types in {}:'.format(usecase))
    df = ref_actions_by_configs(usecase)
    df.drop(columns=['usecase'], inplace=True)
    df.loc[:, REF_ACTIONS.keys()] =\
        df[REF_ACTIONS.keys()].apply(lambda x: round(x, 2))
    df.fillna({c:0 for c in REF_ACTIONS.keys()}, inplace=True)
    df.rename(columns=REF_ACTIONS, inplace=True)
    df['brf_moc'].replace(['1.23', '1.64'], ['no', 'yes'], inplace=True)
    df.rename(columns={'brf_moc': 'brf'}, inplace=True)
    print(df.to_latex(index=False))
    print('\n\n\n')
    return df

def save_plot(fig, filename):
    fig.tight_layout()
    filename = FIGS + filename
    fig.savefig(filename)
    print('Plot saved in: {}'.format(filename))


def plot_ref_actions_shares(df):
    df = df[df[['brf_moc', 'maxeval', 'probpas']].notnull().all(axis=1)]
    df = df.rename(columns=REF_ACTIONS)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.kdeplot(data=df[REF_ACTIONS.values()], fill=True,
            palette='cubehelix', ax=ax)
    ax.set_xlabel('Percentage of refactoring type')
    filename = 'ref_actions_shares_{}.pdf'.format(df.iloc[0]['usecase'])
    save_plot(fig, filename)

def rq4(usecase):
    print_ref_actions_by_configs(usecase)

    plot_ref_actions_shares(ref_actions_by_configs(usecase))

# Train Ticket
rq4('train-ticket')

# Simplified CoCoMe
rq4('simplified-cocome-newrel')
