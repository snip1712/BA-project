<p align="center">
  <img src="https://placehold.co/1200x300/0b1e3d/ffffff?text=British+Airways+Lounge+Analytics" alt="Project Banner" width="100%" />
</p>

<h1 align="center">✈️ British Airways Lounge Eligibility Analytics</h1>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com/?font=Fira+Code&size=22&pause=1000&color=1E3A8A&center=true&vCenter=true&width=600&lines=Forecasting+BA+Lounge+Demand;Pandas+%2B+scikit-learn+%2B+uv;Terminal+3+Capacity+Planning;Data+Science+%E2%80%A2+Forage+Program" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-in--progress-yellow?style=for-the-badge" />
  <img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge" />
</p>

---

## 🛠️ Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white" />
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" />
  <img src="https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white" />
  <img src="https://img.shields.io/badge/uv-6E56CF?style=for-the-badge&logo=python&logoColor=white" />
</p>

---

## 📊 GitHub Stats

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=snip1712&show_icons=true&theme=tokyonight&hide_border=true" width="48%" />
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=snip1712&layout=compact&theme=tokyonight&hide_border=true" width="48%" />
</p>

---

## 🎯 About This Project

Built as part of the **British Airways Data Science (Forage) program**. Since BA plans schedules years into the future — long before specific flight numbers or aircraft assignments exist — this project estimates **lounge tier eligibility** using high-level, scalable flight groupings instead of exact flight details.

| Lounge Tier | Name | Primary Access |
|:---:|:---|:---|
| 🥇 Tier 1 | Concorde Room | First Class · Premier Cardholders · Gold Guest List |
| 🥈 Tier 2 | First Lounge | BA Gold Members |
| 🥉 Tier 3 | Club Lounge | BA Silver Cardholders · Club World (Business) |

---

## 🧠 Thought Process & Trade-offs

This project went through several rounds of "does this actually need to be this complex?" — worth documenting honestly rather than presenting the final code as if it arrived that way.

| Decision Point | Options Considered | What I Chose & Why |
|:---|:---|:---|
| **Data loading** | SQLite cache vs. plain pandas read | Plain read. 10K rows loads fast enough within a working session; a SQLite cache (connection handling, cache invalidation) solved a performance problem I didn't actually have yet. |
| **File path resolution** | Hardcoded convention / folder scan / registry dict | A small registry in `config.py`. Explicit and unambiguous beats clever — no risk of a fuzzy match accidentally picking up a stray file (I hit this for real with a leftover LibreOffice lock file). |
| **Eligibility rate denominator** | Per-tier seat class vs. total passengers on board | Total passengers. The data itself disproved "match by seat class" — thousands of flights had zero first-class seats yet nonzero Tier 1 eligible passengers, so eligibility isn't purely a cabin-class function. |
| **Group averaging method** | Average of per-flight rates vs. sum(eligible) ÷ sum(passengers) | Average of per-flight rates. This represents a *typical* flight in a group, per how the task was framed — the sum-based method would let a handful of large flights dominate the number. |
| **Grouping dimensions** | Region only vs. Region + Haul | Kept both, even though `HAUL` is currently fully determined by `ARRIVAL_REGION` in this dataset. A future schedule could decouple them (e.g. a new short-haul Middle East route), and keeping both costs nothing today. |
| **Small sample groups** | Hierarchical fallback/smoothing vs. flag and move on | Flagged, not solved. The smallest group in this dataset (75 flights) wasn't actually a reliability problem — building smoothing logic for it would have been solving an imagined problem, not a real one. |
| **Aircraft type as a grouping** | Include vs. exclude | Excluded. Its effect (bigger aircraft → more seats) already shows up directly in the seat-count columns, and the task explicitly asked for high-level groupings rather than aircraft-specific ones. |
| **Chart type** | Bar chart vs. heatmap vs. small multiples | Built more than one: a region-comparison bar chart for a quick headline view, and a full heatmap for the complete group-by-group picture (with low-sample groups flagged in orange). Different audiences want different levels of detail. |
| **Region-level summary in charts** | Simple mean of the 4 per-region rows vs. flight-count-weighted mean | Flight-weighted. A straight average would let a region's quiet Lunchtime slot (fewer flights) count exactly as much as its busy Morning slot — weighting by flight count keeps the region number consistent with "average of per-flight rates," the same principle used to build the table itself. |

### 🔭 Future Scaling Notes

- **If the dataset grows dramatically** (multi-year schedules, hundreds of thousands of rows), the SQLite caching idea I set aside is worth revisiting — repeatedly parsing a large spreadsheet would start to actually hurt.
- **The current lookup table only covers combinations present in this schedule.** There's no `Europe + LONG` or `Asia + SHORT` row today because they don't exist yet. If BA schedules a genuinely new combination, the table needs a documented fallback (e.g. falling back to the region's average across all hauls) rather than silently having no answer.
- **This approach infers eligibility from cabin class, not real loyalty data.** If lounge access ever needs to be modeled from actual loyalty-tier records, this dataset doesn't contain that — the current percentages are a reasonable, stated approximation, not ground truth.

---

## ✨ Features

- 📥 **Data loading** — reads the BA summer schedule dataset into pandas
- 🧮 **Rate calculation** — computes per-flight lounge eligibility as a percentage of total passengers on board
- 🗂️ **Group-level lookup table** — averages rates across `ARRIVAL_REGION`, `HAUL`, and `TIME_OF_DAY`
- 📊 **Region comparison chart** — flight-weighted bar chart highlighting the top region per tier
- 🗺️ **Full heatmap** — every group × every tier in one view, with low-sample groups flagged
- 🥯 **Passenger distribution chart** — donut chart of total passenger share by arrival region
- 📤 **CSV export** — *planned, not yet implemented*

---

## 🚀 Installation

This project uses **[uv](https://github.com/astral-sh/uv)** for environment and dependency management.

```bash
# Clone the repo
git clone https://github.com/snip1712/BA-project.git
cd BA-project

# Sync the environment (creates the venv + installs pinned dependencies)
uv sync

# Launch JupyterLab
uv run jupyter lab
```

> **Note:** the raw dataset is not committed to this repo (see `.gitignore`). Place the Forage-provided spreadsheet in `data/` and rename it to **`data.ods`** before running — the current `config.py` expects that exact filename.

Running `data_processing.py` loads the data, builds the lookup table, and generates all charts as PNGs into an `output/` folder at the project root.

---

## 📁 Project Structure

```
BA-project/
├── data/                  # Raw dataset (gitignored) — expects data.ods
├── output/                # Generated chart PNGs (created on run)
├── src/ba_project/
│   ├── __init__.py
│   ├── config.py          # get_data_file_path() / get_output_file_path()
│   ├── data_loader.py     # Spreadsheet loading
│   ├── data_processing.py # Rate calculation + lookup table + runs the charts
│   └── visualization.py   # Region bars, heatmap, passenger pie chart
├── pyproject.toml
├── uv.lock
├── README.md
└── HANDOFF.md
```

---

<p align="center">
  <sub>Built with 🐍 and ☕ as part of the British Airways Data Science Forage program.</sub>
</p>