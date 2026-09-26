# 🏎️ F1 Historical Archive & Analytics Dashboard (1950–Present)

[![Streamlit](https://img.shields.io/badge/Streamlit-1.64.0-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastF1](https://img.shields.io/badge/FastF1-3.8.3-E10600?logo=formula1&logoColor=white)](https://docs.fastf1.dev/)
[![Plotly](https://img.shields.io/badge/Plotly-7.1.0-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![Data Source](https://img.shields.io/badge/Data%20Source-Jolpica--F1%20%2F%20Ergast-blue)](https://github.com/jolpica/jolpica-f1)

An interactive, responsive Formula 1 web dashboard built with **Streamlit**, **FastF1**, and **Plotly**. Explore official race results, grid position changes, and Driver & Constructor World Championship standings across more than seven decades of Formula 1 history (**1950 to present**).

---

## 🌟 Features

- **🏆 Comprehensive Historical Coverage (1950–Present)**: Access race classification and championship standings spanning every season in Formula 1 history.
- **⏱️ Race Summary & Key Metrics**: Instant overview cards for Race Winner, Pole Sitter, Total Starters, and Classified Finishers.
- **📊 Positions Gained / Lost from Grid**: Interactive Plotly bar chart visualizing drivers who surged forward (green) or lost positions (red) relative to their starting grid slot.
- **📋 Full Official Classification**: Clean, structured table showing final position, driver name, constructor, points awarded, status (Finished, +Laps, Retired), and fastest lap times.
- **👑 World Championship Standings**:
  - **Driver Standings**: Top drivers ranked with points progression charts and win tallies.
  - **Constructor Standings**: Team championship rankings from its inception in 1958 onwards.
- **📥 One-Click CSV Export**: Download official classification data for any Grand Prix directly to CSV.
- **⚡ Smart Caching**: Integrated Streamlit and disk caching to ensure near-instantaneous page reloads.

---

## 📂 Project Structure

```text
F1-Data-Dashboard/
├── app.py              # Main Streamlit dashboard application & layout
├── data_loader.py      # Jolpica-F1 / Ergast API queries & FastF1 cache management
├── visualization.py    # Interactive Plotly chart builders (grid delta & standings)
├── analysis.py         # Data processing & lap analytics helpers
├── test.py             # Sandbox & verification scripts
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ installed on your system.

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/F1-Data-Dashboard.git
cd F1-Data-Dashboard
```

### 3. Create a Virtual Environment (Recommended)
```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Launch the Dashboard
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## 🛠️ Tech Stack

- **Frontend & Web Framework**: [Streamlit](https://streamlit.io/)
- **Data Retrieval**: [FastF1](https://docs.fastf1.dev/) with [Jolpica-F1 / Ergast API](https://github.com/jolpica/jolpica-f1)
- **Data Manipulation**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Interactive Visualizations**: [Plotly Express & Graph Objects](https://plotly.com/python/)

---

## 📊 Data Source & Attribution

Data is sourced via **FastF1** and the open-source **Jolpica-F1** project (the community-maintained drop-in successor to the Ergast Developer API).

*Disclaimer: This project is unofficial and is not associated in any way with the Formula 1 companies. F1, FORMULA ONE, FORMULA 1, FIA FORMULA ONE WORLD CHAMPIONSHIP, GRAND PRIX and related marks are trademarks of Formula One Licensing B.V.*

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
