# -*- coding: utf-8 -*-
"""Fig. 2 — dari skrip ChatGPT; panel (a) diubah ke batang horizontal agar nama
kategori muat utuh, dan metrik huruf disetarakan dengan Arial."""
import matplotlib.pyplot as plt
import numpy as np

BARS = {  # category: (SMOTE mean, SMOTE sd, ROS mean, ROS sd), F1 points
    "Botnet": (20.2, 2.23, 7.8, 1.43),
    "PortScan": (6.44, 0.87, 1.62, 0.37),
    "Web Attack": (-0.56, 0.67, -2.81, 0.21),
    "Infiltration": (5.23, 0.23, 1.65, 1.84),
    "DoS": (1.02, 0.27, 0.87, 0.2),
    "DDoS": (0.54, 0.45, 0.45, 0.48),
}

POINTS = {  # category: [[synthetic intrusion %, SMOTE F1 gain], ...] — 15 subsets each
    "Botnet": [[37.5, 19.31], [37.5, 25.48], [28.8, 16.03], [38.2, 18.9], [28.1, 9.55], [29.6, 19.15], [33.1, 21.32], [34.2, 19.54], [37.0, 19.75], [36.3, 18.64], [39.1, 17.86], [33.1, 26.68], [22.8, 20.5], [30.1, 16.85], [36.8, 30.98]],
    "PortScan": [[33.9, 4.37], [28.7, 6.41], [23.6, 4.72], [32.8, 3.75], [25.6, 11.26], [28.3, 2.42], [21.6, 9.13], [26.2, 2.34], [33.3, 6.92], [30.4, 8.49], [24.4, 8.52], [35.9, 1.05], [32.1, 7.82], [23.5, 9.2], [31.2, 11.37]],
    "Web Attack": [[17.3, 1.37], [13.1, -2.93], [10.4, 0.41], [15.0, -2.79], [13.2, 4.06], [19.0, 0.8], [15.4, -2.12], [15.9, 0.41], [10.2, 0.28], [14.8, -2.11], [1.2, -2.38], [14.0, 1.04], [16.2, -0.77], [14.8, -5.03], [10.8, 0.39]],
    "Infiltration": [[12.6, 0.0], [16.3, 0.0], [16.8, 0.0], [15.2, 14.29], [12.2, 10.61], [15.8, 0.0], [12.2, 12.73], [15.7, 0.0], [13.3, 7.62], [17.7, 7.69], [16.6, 0.0], [16.8, 0.0], [7.8, 12.73], [15.8, 0.0], [15.2, 15.38]],
    "DoS": [[12.8, 2.38], [17.1, -0.03], [9.3, 0.16], [15.9, -0.39], [10.4, 2.41], [4.3, 1.52], [9.3, 0.94], [14.7, 0.61], [11.7, -0.64], [7.5, 1.63], [8.3, 0.73], [15.3, 0.76], [23.9, 3.02], [10.1, 1.64], [10.9, 0.44]],
    "DDoS": [[1.5, 0.53], [2.4, 0.25], [0.4, 4.02], [4.1, -0.61], [0.7, 1.23], [1.9, 0.25], [5.2, -0.52], [0.7, 0.71], [0.9, 0.76], [2.8, 0.03], [2.1, 0.83], [1.0, -0.38], [2.9, 1.04], [2.2, -0.35], [1.9, 0.44]],
}

# Liberation Sans punya metrik identik dengan Arial; nama "Arial" ditulis ke SVG
# setelahnya, sehingga tata letaknya benar dan penerbit menerima nama yang diharapkan.
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "Liberation Sans"
plt.rcParams["font.size"] = 8
plt.rcParams["text.color"] = "#333333"
plt.rcParams["axes.labelcolor"] = "#333333"
plt.rcParams["axes.titlecolor"] = "#333333"

categories = list(BARS)
assert list(POINTS) == categories and len(categories) == 6
assert sum(map(len, POINTS.values())) == 90

fig, (axL, axR) = plt.subplots(1, 2, figsize=(6.97, 2.95),
                               gridspec_kw={"width_ratios": [1, 1.18]})
# margin diatur tangan, bukan bbox tight, supaya lebarnya tetap persis 6,5 inci
fig.subplots_adjust(left=0.108, right=0.715, bottom=0.175, top=0.875, wspace=0.40)

def style(ax, value_axis):
    ax.set_axisbelow(True)
    ax.grid(axis=value_axis, color="#E6E6E6", linewidth=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#666666"); ax.spines[s].set_linewidth(0.8)
    ax.tick_params(colors="#333333", labelsize=8, width=0.8, length=3)

# ---- panel (a): batang horizontal, kategori di sumbu tegak --------------------
style(axL, "x")
y = np.arange(len(categories))[::-1]
h = 0.36
ek = dict(ecolor="#333333", elinewidth=0.8, capthick=0.8)
axL.barh(y + h/2, [BARS[k][0] for k in categories], h,
         xerr=[BARS[k][1] for k in categories], capsize=2, error_kw=ek,
         color="#0072B2", label="SMOTE", zorder=2.5)
axL.barh(y - h/2, [BARS[k][2] for k in categories], h,
         xerr=[BARS[k][3] for k in categories], capsize=2, error_kw=ek,
         color="#D55E00", label="Random\noversampling", zorder=2.5)
axL.axvline(0, color="#333333", linewidth=0.8, zorder=1.5)
axL.set_yticks(y); axL.set_yticklabels(categories, fontsize=8)
axL.set_ylim(-0.6, len(categories) - 0.4)
axL.set_xlim(-4.0, 25.0)   # ruang di kanan untuk legenda, jauh dari batang
axL.set_xlabel("F1 gain over no resampling (points)", fontsize=8.5)
axL.set_title("(a) Gain at 29 training samples", fontsize=9, fontweight="bold", pad=6)
axL.legend(loc="lower right", frameon=False, fontsize=8, handlelength=1.1,
           handletextpad=0.4, labelspacing=0.5, borderaxespad=0.1)

# ---- panel (b): tidak diubah --------------------------------------------------
style(axR, "y")
marks = {"Botnet": ("#0072B2", "o"), "PortScan": ("#E69F00", "s"),
         "Web Attack": ("#009E73", "^"), "Infiltration": ("#56B4E9", "D"),
         "DoS": ("#CC79A7", "v"), "DDoS": ("#D55E00", "P")}
for name in categories:
    c, m = marks[name]
    axR.scatter([p[0] for p in POINTS[name]], [p[1] for p in POINTS[name]],
                s=22, c=c, marker=m, edgecolors="white", linewidths=0.4,
                alpha=0.9, label=name, zorder=3)
axR.axhline(0, color="#333333", linewidth=0.8, zorder=1.5)
axR.set_xlabel("Synthetic intrusion of the 29-sample subset (%)", fontsize=8.5)
axR.set_ylabel("SMOTE gain in F1 (points)", fontsize=8.5)
axR.set_title("(b) Per-subsample geometry against gain", fontsize=9,
              fontweight="bold", pad=6)
axR.legend(ncol=2, loc="upper left", bbox_to_anchor=(1.03, 1.02), frameon=False,
           fontsize=8, handlelength=0.8, handletextpad=0.35,
           columnspacing=0.6, labelspacing=0.6, borderaxespad=0)

fig.savefig("fig2.svg")
plt.close(fig)

# nama keluarga huruf ditulis ulang: metrik Liberation Sans = metrik Arial
s = open("fig2.svg").read().replace("'Liberation Sans'", "Arial, Helvetica, sans-serif")
open("fig2.svg", "w").write(s)
print("fig2.svg ditulis")
