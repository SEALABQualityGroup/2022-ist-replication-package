import numpy as np

import pandas as pd

case_studies = {'train-ticket', 'simplified-cocome-newrel'}
objetives_dir = "../data/objectives"
paretos_dir = "../data/paretos"
q_indicators_dir = "../data/quality_indicators"


def read_csv(file):
    return pd.read_csv(q_indicators_dir + "/{}.csv".format(file))


def extract_best_indicator(file, n=5):
    df = read_csv(file)
    column_names = ['case_study', 'brf', 'max_eval', 'prob_pas', 'q_indicator', 'value']
    df_best_qi_value = pd.DataFrame(columns=column_names)

    for cs in ['train-ticket', 'simplified-cocome', 'simplified-cocome-newrel']:
        df_ucs = df[df["case_study"] == cs].astype({'value': 'float'})
        for qi in ['HV', 'IGD+', 'EP', 'GSPREAD']:
            asc = True
            if qi == 'HV':
                asc = False

            df_uc = df_ucs[df_ucs["q_indicator"] == qi].sort_values(by='value', ascending=asc)
            df_best_qi_value = df_best_qi_value.append(df_uc.head(n))
    return df_best_qi_value


output_dir ='../data/analysis_results'
n = 5
file = "qi"
extract_best_indicator(file, n).to_csv(output_dir+"/best_{}_{}_cs.csv".format(n, file), encoding='utf-8')
file = "qi__no_pas"
extract_best_indicator(file, n).to_csv(output_dir+"/best_{}_{}_cs.csv".format(n, file), encoding='utf-8')
