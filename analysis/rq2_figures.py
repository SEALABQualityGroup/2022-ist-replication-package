import pandas as pd
import pareto as pr
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

def gen_stats(usecase, rel):
    params = {'brf_moc': '1.64', 'probpas': '0.95', 'usecase': usecase}
    p1 = pr.get_paretos(params)

    params["brf_moc"] = '1.23'
    p2 = pr.get_paretos(params)

    paretos = p1 + p2
    df = create_dataframe(paretos, rel)

    print("\nMedian: \n", df.median())
    print("\nMean: \n", df.mean())

    improv = df.loc[(df['reliability'] >= rel)]

    sma_perfQ = improv.nsmallest(3, "perfQ")
    lar_perfQ = improv.nlargest(3, "perfQ")

    sma_rel = improv.nsmallest(3, "reliability")
    lar_rel = improv.nlargest(3, "reliability")

    improvment = lambda old, new: (new-old)/old*100

    print("\nSmallestPerfQ: \n", sma_perfQ)
    print("\nLargestPerfQ: \n", lar_perfQ)

    print("\nSmallestRel: \n", sma_rel)
    print("\nLargestRel: \n", lar_rel)
    print("\nImprovementRel (Interval): \n",
      improvment(sma_rel.iloc[0]["reliability"], sma_rel.iloc[1]["reliability"]),
      improvment(sma_rel.iloc[0]["reliability"], lar_rel.iloc[0]["reliability"])
    )

    det = df.loc[df['reliability'] < rel]
    print("\namount of solutions: ", len(df), "\nimproving the initial solution: ", len(improv), "\nworse than the initial solution: ", len(det), '\n')

    gen_scatter(df, usecase, rel)

    return improv

def create_dataframe(files, rel):
    df = pd.DataFrame()

    for x in files:
        df = df.append(pd.read_csv(x.file))

    df = df.drop(['solID'], axis=1).reindex()
    df = abs(df)
    df = df.append(
        {
            'perfQ': 0.0, '#changes': 0.0, 'pas': 0.0, 'reliability': rel
        }, ignore_index=True
    )

    return df

def gen_scatter(df, usecase, rel):
    colors = np.where((df['reliability'] >= rel) & (df['perfQ'] > 0.000000), 'k', 'y')
    scatter_plt = df.plot.scatter(x="perfQ", y="reliability", c=colors)
    scatter_plt.annotate("initial", fontsize=14, xy=(0.0, rel), xycoords='data',
            xytext=(12, -12), textcoords='offset points', ha="left", va="center",
            arrowprops=dict(arrowstyle="wedge,tail_width=.01", facecolor='black'))

    with PdfPages("../figs/"+usecase+".pdf") as pdf:
        fig = scatter_plt.get_figure()
        pdf.savefig(fig)

    print(
        ("Scatter showing the solutions improving realiability and performance generated at "
        "../figs/"+usecase+".pdf")
    )

def merge_super_paretos(improv, p1, p2):
    sp1 = pr.Pareto(p1)
    sp2 = pr.Pareto(p2)

    sp1_df = sp1.read_rf()
    sp2_df = sp1.read_rf()

    sp = sp1_df.append(sp2_df)

    mrg = sp.merge(improv, on=["perfQ", "reliability"], how="inner")

    # left excluding merge
    left = sp.merge(improv, on=["perfQ", "reliability"], how="left", indicator=True).query('_merge == "left_only"').drop('_merge', 1)
    print("super-pareto size: ", len(sp), "solutions taken from analyzed paretos:", len(mrg))

tt_sp1 = "../data/reference_paretos/train-ticket__super_pareto__BRF_moc_1.23_ProbPAs_0.95__Algo_nsgaii.rf"
tt_sp2 = "../data/reference_paretos/train-ticket__super_pareto__BRF_moc_1.64_ProbPAs_0.95__Algo_nsgaii.rf"

improv = gen_stats("train-ticket", 0.657925)
merge_super_paretos(improv, tt_sp1, tt_sp2)

cc_sp1 = "../data/reference_paretos/simplified-cocome-newrel__super_pareto__BRF_moc_1.23_ProbPAs_0.95__Algo_nsgaii.rf"
cc_sp2 = "../data/reference_paretos/simplified-cocome-newrel__super_pareto__BRF_moc_1.64_ProbPAs_0.95__Algo_nsgaii.rf"

improv = gen_stats("simplified-cocome-newrel", 0.763062)
merge_super_paretos(improv, cc_sp1, cc_sp2)
