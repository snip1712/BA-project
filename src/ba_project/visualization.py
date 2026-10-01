

"""Charts for the BA lounge-eligibility lookup table.

Expects the flat lookup table (``reset_index()`` shape) with these columns:
ARRIVAL_REGION, HAUL, TIME_OF_DAY, t1_mean, t2_mean, t3_mean, count

Usage:
    from ba_project.visualization import create_visualizations
    paths = create_visualizations(lookup_df)
"""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure

from ba_project.config import get_output_file_path as get_output

logging.basicConfig(level=logging.INFO)
# --- Column names ------------------------------------------------------------------------------------------
REGION, HAUL, TOD, COUNT = "ARRIVAL_REGION", "HAUL", "TIME_OF_DAY", "count"
TIERS = {
    "t1_mean": ("Tier 1", "Highest access (First / Premier / Gold)"),
    "t2_mean": ("Tier 2", "Mid-level access"),
    "t3_mean": ("Tier 3", "Broadest access"),
}
TOD_ORDER = ["Morning", "Lunchtime", "Afternoon", "Evening"]
LOW_SAMPLE = 100  # groups with fewer flights are flagged
PAX_COLS = ["FIRST_CLASS_SEATS", "BUSINESS_CLASS_SEATS", "ECONOMY_SEATS"]


# --- Palette ----------------------------------------------------------------------------------
INK, MUTE, LINE = "#0f1f1d", "#5f6f6d", "#e4eae9"
ACCENT, ACCENT_SOFT, WARN = "#0e8f80", "#a9d6cf", "#c2571a"
HEAT_CMAP = LinearSegmentedColormap.from_list("lounge", ["#f1f8f7", "#5bb5a8"])

_RC = {
    "font.family": "sans-serif",
    "font.sans-serif": ["IBM Plex Sans", "Helvetica Neue", "Arial", "DejaVu Sans"],
    "font.serif": ["Source Serif 4", "Georgia", "DejaVu Serif"],
    "text.color": INK,
    "axes.edgecolor": LINE,
    "figure.facecolor": "white",
}



# --- Helpers ----------------------------------------------------------------------------------
def _output_dir() -> Path:
    """Return <get_output()>/output, creating it if needed.

    If get_output() already points at a folder called "output", use it as is.
    """
    base = get_output()
    out = base if base.name == "output" else base / "output"
    out.mkdir(parents=True, exist_ok=True)
    return out


def _validate(df: pd.DataFrame) -> None:
    needed = {REGION, HAUL, TOD, COUNT, *TIERS}
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"Lookup table is missing columns: {sorted(missing)}")


def _sorted(df: pd.DataFrame) -> pd.DataFrame:
    """Sort by region, then time of day in clock order (not alphabetical)."""
    out = df.copy()
    out[TOD] = pd.Categorical(out[TOD], categories=TOD_ORDER, ordered=True)
    return out.sort_values([REGION, TOD]).reset_index(drop=True)


def _region_means(df: pd.DataFrame, col: str) -> pd.Series:
    """Flight-weighted mean per region (exact mean of per-flight rates)."""
    weighted = (df[col] * df[COUNT]).groupby(df[REGION]).sum()
    return (weighted / df[COUNT].groupby(df[REGION]).sum()).sort_values()


# --- Chart 1: region comparison ---------------------------------------------
def plot_region_bars(df: pd.DataFrame) -> Figure:
    """One horizontal-bar panel per tier, comparing arrival regions."""
    _validate(df)
    with plt.rc_context(_RC):
        fig, axes = plt.subplots(1, 3, figsize=(13, 4.6))
        fig.suptitle(
            "Europe short-haul flights carry the highest share in every tier",
            x=0.02, ha="left", fontsize=17, fontweight="bold", family="serif",
        )
        fig.text(0.02, 0.885, "Average % of passengers eligible, by arrival region "
                 "(each tier has its own scale)", color=MUTE, fontsize=10.5)

        for ax, (col, (title, note)) in zip(axes, TIERS.items()):
            s = _region_means(df, col)
            colors = [ACCENT_SOFT] * (len(s) - 1) + [ACCENT]  # highlight the top bar
            ax.barh(s.index, s.values, color=colors, height=0.62)
            decimals = 2 if col == "t1_mean" else 1
            for y, v in enumerate(s.values):
                ax.text(v + s.max() * 0.02, y, f"{v:.{decimals}f}%",
                        va="center", fontsize=10, fontweight="normal")
            ax.set_xlim(0, s.max() * 1.22)
            ax.set_title(f"{title}\n", loc="left", fontsize=12, fontweight="bold")
            ax.text(0, 1.02, note, transform=ax.transAxes, color=MUTE, fontsize=9)
            ax.set_xticks([])
            ax.tick_params(axis="y", length=0, labelsize=10)
            for side in ("top", "right", "bottom"):
                ax.spines[side].set_visible(False)

        fig.tight_layout(rect=(0, 0, 1, 0.87))
    return fig


# --- Chart 2: heatmap of all groups -----------------------------------------
def plot_heatmap(df: pd.DataFrame) -> Figure:
    """Heatmap of every region/time-of-day group across the three tiers.

    Shading is scaled within each tier column, so Tier 1 (~0.2%) is as
    readable as Tier 3 (~11-17%).
    """
    _validate(df)
    d = _sorted(df)
    cols = list(TIERS)
    values = d[cols].to_numpy(dtype=float)
    norm = (values - values.min(0)) / (values.max(0) - values.min(0))
    n = len(d)

    with plt.rc_context(_RC):
        fig, ax = plt.subplots(figsize=(11, 0.46 * n + 2.2))
        ax.imshow(norm, cmap=HEAT_CMAP, aspect="auto", vmin=0, vmax=1)

        # white cell gaps
        ax.set_xticks(np.arange(-0.5, 3), minor=True)
        ax.set_yticks(np.arange(-0.5, n), minor=True)
        ax.grid(which="minor", color="white", linewidth=2)
        ax.tick_params(which="both", length=0)

        # cell values
        for i in range(n):
            for j, col in enumerate(cols):
                ax.text(j, i, f"{values[i, j]:.{3 if j == 0 else 2}f}",
                        ha="center", va="center", fontsize=10.5)

        # column headers + flights column
        ax.xaxis.tick_top()
        ax.set_xticks(range(3), [f"{t[0]} %" for t in TIERS.values()],
                      fontsize=11, fontweight="bold", color=MUTE)
        ax.text(3.25, -0.78, "Flights", ha="right", va="center",
                fontsize=11, fontweight="bold", color=MUTE)
        for i, c in enumerate(d[COUNT]):
            low = c < LOW_SAMPLE
            ax.text(3.25, i, f"{c:,}", ha="right", va="center", fontsize=10.5,
                    color=WARN if low else INK, fontweight="bold" if low else "normal")

        # time-of-day labels + region blocks
        ax.set_yticks(range(n), d[TOD].astype(str), fontsize=10.5)
        ytx = ax.get_yaxis_transform()
        start = 0
        for region, grp in d.groupby(REGION, sort=False):
            end = start + len(grp) - 1
            mid = (start + end) / 2
            ax.text(-0.36, mid - 0.12, region, transform=ytx, ha="right",
                    va="center", fontsize=12, fontweight="bold")
            ax.text(-0.36, mid + 0.38, f"{grp[HAUL].iloc[0].title()}-haul",
                    transform=ytx, ha="right", va="center", fontsize=9.5, color=MUTE)
            if end < n - 1:
                ax.axhline(end + 0.5, color=MUTE, linewidth=1.2, xmax=1.0,
                           xmin=-0.41, clip_on=False)
            start = end + 1

        ax.set_xlim(-0.5, 3.3)
        for s in ax.spines.values():
            s.set_visible(False)

        fig.suptitle("The full picture: all flight types", x=0.02, ha="left",
                     fontsize=17, fontweight="bold", family="serif")
        fig.text(0.02, 0.93 if n > 8 else 0.9,
                 "Darker cells are higher within their own tier column",
                 color=MUTE, fontsize=10.5)
        fig.text(0.02, 0.015,
                 f"Rate = eligible passengers / total on board x 100, per flight, then averaged. "
                 f"Orange = fewer than {LOW_SAMPLE} flights; read with caution.",
                 color=MUTE, fontsize=9)
        fig.subplots_adjust(left=0.29, right=0.97, top=0.85, bottom=0.05)
    return fig

#--- chart 3: passenger pie chart -----------------------------------------
def plot_passenger_pie(raw_df: pd.DataFrame) -> Figure:
    """Donut chart: each arrival region's share of all passengers.

    Takes the RAW flight-level DataFrame, not the lookup table.
    """
    missing = {REGION, *PAX_COLS} - set(raw_df.columns)
    if missing:
        raise ValueError(f"Raw data is missing columns: {sorted(missing)}")

    s = (raw_df[PAX_COLS].sum(axis=1)
         .groupby(raw_df[REGION]).sum()
         .sort_values(ascending=False))
    cmap = LinearSegmentedColormap.from_list("donut", [ACCENT, "#d6ebe8"])
    colors = cmap(np.linspace(0, 1, len(s)))

    with plt.rc_context(_RC):
        fig, ax = plt.subplots(figsize=(8, 5))
        wedges, _ = ax.pie(
            s.values, colors=colors, startangle=90, counterclock=False,
            wedgeprops=dict(width=0.38, edgecolor="white", linewidth=2),
        )
        ax.legend(
            wedges, [f"{r}   {v / s.sum():.0%}" for r, v in s.items()],
            loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False, fontsize=12,
        )
        ax.text(0, 0, f"{s.sum():,.0f}\npassengers", ha="center", va="center",
                fontsize=15, fontweight="bold")
        ax.set_title("Where our passengers arrive", loc="left", fontsize=17,
                     fontweight="bold", family="serif")
    return fig

# --- The entry point ------------------------------------------------------------
def create_visualizations(raw : pd.DataFrame, df: pd.DataFrame, dpi: int = 200) -> dict[str, Path]:
    """Build every chart and save PNGs into <get_output()>/output.
    ARGs:
        raw: the raw flight-level DataFrame (for the passenger pie chart)
        df: the lookup table (reset_index() shape) with the seven columns
        dpi: resolution for saved PNGs
    Returns {chart_name: saved_path}.
    """
    out = _output_dir()
    charts = {
        "region_bars": plot_region_bars(df),
        "heatmap": plot_heatmap(df),
    }
    paths = {}
    for name, fig in charts.items():
        path = out / f"lounge_{name}.png"
        fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        logging.info(f"Saving {name} chart to {out}")
        paths[name] = path
    
    fig = plot_passenger_pie(raw)            
    fig.savefig(_output_dir() / "passenger_pie.png",
            dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    logging.info(f"Saving passenger pie chart to {out}")
    paths["passenger_pie"] = _output_dir() / "passenger_pie.png"
    return paths
