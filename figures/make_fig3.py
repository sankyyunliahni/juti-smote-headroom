import matplotlib.pyplot as plt
from matplotlib import font_manager, ticker
from pathlib import Path
import re

# Measured experimental results: means and standard deviations over three seeds.
# Every measurement is reproduced exactly, in its original order.
CURVE = {
    "n_per_class": [1000, 5000, 10000, 24000, 40000, 60000, 80000, 128484],
    "Infiltration recall": {"mean": [53.59, 54.93, 55.26, 55.93, 56.53, 56.70, 57.10, 57.44], "sd": [0.64, 0.66, 0.60, 0.64, 0.33, 0.27, 0.17, 0.23]},
    "Infiltration precision": {"mean": [55.00, 56.32, 57.06, 57.46, 57.63, 57.68, 57.74, 57.61], "sd": [0.25, 0.25, 0.21, 0.39, 0.14, 0.22, 0.21, 0.08]},
    "Infiltration F1": {"mean": [54.29, 55.62, 56.14, 56.69, 57.07, 57.18, 57.42, 57.52], "sd": [0.22, 0.40, 0.32, 0.48, 0.17, 0.25, 0.17, 0.11]},
    "BENIGN recall": {"mean": [56.15, 57.39, 58.42, 58.59, 58.44, 58.40, 58.21, 57.73], "sd": [0.94, 0.54, 0.59, 0.48, 0.37, 0.19, 0.30, 0.23]},
}

# Resolve using Arial metrics when possible, while keeping text searchable.
installed = {font.name for font in font_manager.fontManager.ttflist}
font_family = next(
    (name for name in ("Arial", "Liberation Sans", "DejaVu Sans") if name in installed),
    "DejaVu Sans",
)
plt.rcParams.update({
    "svg.fonttype": "none",
    "font.family": font_family,
    "font.size": 8,
    "axes.labelsize": 8.5,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.labelcolor": "#333333",
    "text.color": "#333333",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "axes.edgecolor": "#666666",
    "axes.linewidth": 0.8,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})

styles = {
    "Infiltration recall": ("#0072B2", "o", "-"),
    "Infiltration precision": ("#E69F00", "s", "--"),
    "Infiltration F1": ("#009E73", "^", "-."),
    "BENIGN recall": ("#D55E00", "D", ":"),
}

x = CURVE["n_per_class"]
assert len(x) == 8
assert list(CURVE)[1:] == list(styles)
assert all(
    len(CURVE[series][kind]) == 8
    for series in styles
    for kind in ("mean", "sd")
)

fig, ax = plt.subplots(figsize=(6.97, 2.25))
# Explicit margins preserve the exact 6.97-inch exported canvas width.
fig.subplots_adjust(left=0.085, right=0.985, bottom=0.315, top=0.955)

ax.set_xscale("log")
ax.set_xlim(800, 180000)
ax.set_ylim(0, 100)
ax.set_xticks([1000, 10000, 100000])
ax.xaxis.set_major_formatter(ticker.FixedFormatter(["1,000", "10,000", "100,000"]))
ax.xaxis.set_minor_locator(ticker.NullLocator())
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))

ax.set_axisbelow(True)
ax.grid(axis="y", color="#E6E6E6", linewidth=0.6)
ax.grid(axis="x", visible=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color("#666666")
    ax.spines[side].set_linewidth(0.8)
ax.tick_params(axis="both", which="major", colors="#333333", labelsize=8,
               width=0.8, length=3, direction="out")

ax.axhline(50, color="#888888", linewidth=0.9,
           linestyle=(0, (4, 3)), zorder=1.5)
ax.text(1100, 48.4, "chance level on a balanced task",
        fontsize=7.5, color="#666666", ha="left", va="top", zorder=2)

for name, (color, marker, line_style) in styles.items():
    ax.errorbar(
        x, CURVE[name]["mean"], yerr=CURVE[name]["sd"],
        label=name, color=color, linestyle=line_style, marker=marker,
        linewidth=1.4, markersize=4, markerfacecolor=color,
        markeredgecolor="white", markeredgewidth=0.4,
        ecolor=color, elinewidth=0.8, capsize=2, capthick=0.8,
        zorder=3,
    )

ax.set_xlabel(
    "BENIGN and Infiltration training samples per class (1:1 ratio, log scale)",
    fontsize=8.5, color="#333333", labelpad=7,
)
ax.set_ylabel("Percentage (%)", fontsize=8.5, color="#333333", labelpad=7)
legend = ax.legend(loc="upper left", ncol=2, frameon=False, fontsize=8,
                   columnspacing=1.2, handlelength=2.4,
                   handletextpad=0.6, labelspacing=0.6, borderaxespad=0.5)
for label in legend.get_texts():
    label.set_color("#333333")

output = Path(__file__).with_name("fig3.svg")
fig.savefig(output, format="svg")  # Intentionally no bbox_inches='tight'.
plt.close(fig)

# Leave text as <text> elements and publish with the requested font stack.
svg = output.read_text(encoding="utf-8")
font_pattern = re.compile(
    r"(?<![\w-])(?:'|&apos;|\")?"
    + re.escape(font_family)
    + r"(?:'|&apos;|\")?(?![\w-])"
)
svg = font_pattern.sub("Arial, Helvetica, sans-serif", svg)
output.write_text(svg, encoding="utf-8")
