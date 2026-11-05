# Detection headroom, not minority-class geometry, predicts SMOTE gains

Notebooks, run configurations, and result files for the paper submitted to *JUTI: Jurnal Ilmiah
Teknologi Informasi*.

Every table in the paper is computed from a file in `results/`, not transcribed by hand. The map
below gives the file behind each one, so any number in the paper can be checked without repeating
the computation.

## Datasets

Neither dataset is redistributed here. Both are obtained from the Canadian Institute for
Cybersecurity:

- CIC-IDS2017 — <https://www.unb.ca/cic/datasets/ids-2017.html>
- CSE-CIC-IDS2018 — <https://www.unb.ca/cic/datasets/ids-2018.html>

The notebooks download and clean them, then cache the cleaned arrays as `clean_data.npz` so that
later runs skip the download. De-duplication happens before anything else, so record counts differ
from the raw releases: 124,127 for CIC-IDS2017 after capping each category at 30,000.

## Notebooks

Run them in this order. Each writes checkpoint files and can be interrupted and resumed: re-run
the same cell and it skips the work already done.

| Notebook | What it produces | Approximate time |
|---|---|---|
| `JUTI_rerun_v3.ipynb` | Base-model selection, the controlled experiment at 29 samples across three classifier families, subset geometry, feature-space complexity, error destinations | ~11 h |
| `JUTI_rerun_v4_cse2018.ipynb` | CSE-CIC-IDS2018: controlled experiment, geometry, Infiltration learning curve | ~6 h |
| `JUTI_ablasi_v5.ipynb` | Sample-size ablation at 29/50/100/500 on nested subsets; SMOTE parameter sensitivity | ~8 h + 2.6 h |
| `JUTI_headroom_v6.ipynb` | Capacity ablation with the subsets held fixed; geometry recomputed at each subset size | ~2.5 h + 50 min |

Timings are for the two-core machines Google Colab allocated; `TIME_BUDGET_MIN` stops a cell
cleanly before the session is cut off.

## Which file produces which table

| Paper | Source file |
|---|---|
| Table 3, Table 4, Fig. 2 | `secC_controlled_v2.csv`, `secC_subsample_shape.csv` |
| Table 5 | `k1.csv`, `k2.csv` |
| Table 6, Table 7 | `secC_subsample_shape.csv`, `secJ_synthetic_destination.csv` |
| Table 8 | `k2.csv` with `secC_subsample_shape.csv` |
| Table 9 | `secJ_synthetic_destination.csv` |
| Table 10 | `secX_capacity.csv`, `v6_capacity_summary.csv` |
| Table 11 | `secT_ablation.csv`, `v5_ablation_summary.csv` |
| Table 12 | `secV_smote_sensitivity.csv`, `v5_sensitivity_detail.csv` |
| Table 13 | `secI_complexity.csv` |
| Table 14 | `secH_error_destination.csv`, `secH_new.csv` |
| Table 16, Fig. 3 | `secE_cse2018_curve.csv` |
| Section 4.7 geometry by subset size | `secY_geometry_by_size.csv`, `v6_grid_summary.csv` |
| CSE-CIC-IDS2018 controlled experiment | `secP_controlled_cse2018.csv`, `secQ_*.csv`, `v4_pooled_summary.csv` |

## Seeds and determinism

The principal experiment uses seeds 42, 43, and 44 with five folds. The robustness experiments of
Sections 4.7 and 4.8 use seed 42 only, which is stated in the paper because it limits what the
paired tests on them can resolve.

One caveat on exact reproduction, documented in Section 4.7 of the paper. XGBoost with
`tree_method="hist"` and `n_jobs=-1` accumulates histogram gradients in an order that depends on
the thread count, so a machine with a different number of cores can produce slightly different
trees on the larger resampled training sets. In our own runs this affected 2 of 60 comparisons,
by at most 24 detections out of 6,000. The unresampled condition reproduced exactly in all 60.

## Licence

Code released under the MIT Licence. The datasets keep the licence terms set by the Canadian
Institute for Cybersecurity.

## Aggregation conventions

Two conventions matter when regenerating the tables from `results/`.

**Share of missed attacks recovered (Rc).** For each category, the false-negative counts of
the five folds of a seed are pooled *before* the ratio `100*(FN_base - FN_smote)/FN_base` is
formed; the three seed values are then averaged. Averaging a ratio computed fold by fold is
not equivalent: where a fold holds very few missed attacks the denominator is near zero, and
for DDoS the two conventions differ by more than forty points (+34.8 pooled against -13.6
per fold). Tables 4, 7 and 8 of the paper all use the pooled convention.

**F1 aggregation.** Table 3 pools the confusion counts of the five folds of a seed before
computing F1 and reports the mean over seeds. Table 5 computes F1 inside each of the fifteen
fold-and-seed observations and averages those; this is the quantity the paired tests operate
on. The two differ by at most 0.1 points for five of the six categories and by 1.0 point for
Infiltration, whose folds hold seven or eight test records.

## Figures

`figures/fig1_research_workflow.svg` is the vector source of Fig. 1, and
`figures/make_fig1.py` regenerates it; the script measures text with the font metrics so that
no label can overflow its box.
