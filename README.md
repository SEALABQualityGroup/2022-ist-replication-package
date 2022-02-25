#### Replication package for the paper:

*Many-Objective Optimization of Non-Functional Attributes based on Refactoring of Software Models*\
by Vittorio Cortellessa, Daniele Di Pompeo, Vincenzo Stoico, Michele Tucci

#### How to generate the tables and figures in the paper
Initialize the python execution environment:
```bash
git clone https://github.com/SEALABQualityGroup/2022-ist-replication-package
cd 2022-ist-replication-package
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The `analysis` folder contains scripts for each research question:
```bash
cd analysis
python rq1_tables_quality_indicator_stats.py
python rq1.1_rq1.3_figures.py
python rq1.2_figures.py
python rq2_figures.py
python rq3_tables_and_figures.py
```
