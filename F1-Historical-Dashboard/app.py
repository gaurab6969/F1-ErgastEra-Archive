import streamlit as st
import pandas as pd

from data_loader import (
    get_race_names,
    get_round_number,
    get_historical_race_results,
    get_driver_standings,
    get_constructor_standings
)

from visualization import (
    historical_grid_vs_finish_chart,
    historical_standings_chart
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="F1 Historical Results & Standings",
    page_icon="🏎️",
    layout="wide"
)


# =========================================================
# TITLE & HEADER
# =========================================================

st.title("🏎️ F1 Historical Archive (1950–Present)")

st.markdown(
    """
    Explore official race results, grid changes, and championship standings
    across more than seven decades of Formula 1 history, powered by the Jolpica-F1 / Ergast API.
    """
)


# =========================================================
# SIDEBAR CONTROLS
# =========================================================

st.sidebar.header("🏁 Race Selection")

years_list = list(range(2026, 1949, -1))
default_year_index = years_list.index(2026) if 2026 in years_list else 0

year = st.sidebar.selectbox(
    "Season",
    years_list,
    index=default_year_index,
    help="Select any Formula 1 season from 1950 to the present."
)


# =========================================================
# GET RACE SCHEDULE
# =========================================================

try:
    race_names = get_race_names(year)
except Exception as error:
    st.error(f"Could not retrieve race schedule: {error}")
    st.stop()

if not race_names:
    st.warning("No races were found for this season.")
    st.stop()


default_gp_index = 0
for i, name in enumerate(race_names):
    if "Monaco" in name:
        default_gp_index = i
        break

grand_prix = st.sidebar.selectbox(
    "Grand Prix",
    race_names,
    index=default_gp_index
)

round_num = get_round_number(year, grand_prix)

st.sidebar.divider()
st.sidebar.markdown(
    f"""
    **🏆 Current Selection:**
    - **Season:** {year}
    - **Grand Prix:** {grand_prix}
    - **Round:** {round_num} of {len(race_names)}
    """
)


# =========================================================
# MAIN CONTENT TABS
# =========================================================

st.subheader(f"🏆 {year} {grand_prix}")

tab_race, tab_standings = st.tabs([
    "🏁 Race Classification & Grid Changes",
    "👑 Season Championship Standings"
])


# =========================================================
# TAB 1: RACE CLASSIFICATION
# =========================================================

with tab_race:
    with st.spinner("Fetching race results from Jolpica-F1..."):
        results_df = get_historical_race_results(year, round_num)

    if not results_df.empty:
        # Highlight Metric Cards
        col1, col2, col3, col4 = st.columns(4)

        winner_row = results_df.iloc[0]
        winner_name = winner_row.get("DriverName", winner_row.get("driverId", "N/A"))
        winner_team = winner_row.get("constructorName", "")

        pole_row = results_df[results_df["grid"] == 1]
        pole_driver = pole_row.iloc[0].get("DriverName", pole_row.iloc[0].get("driverId", "N/A")) if not pole_row.empty else "N/A"

        finishers = len(results_df[results_df["status"] == "Finished"])

        with col1:
            st.metric("Winner 🥇", winner_name, winner_team)
        with col2:
            st.metric("Pole Position ⏱️", pole_driver)
        with col3:
            st.metric("Total Starters 🏎️", len(results_df))
        with col4:
            st.metric("Classified Finishers 🏁", finishers)

        st.divider()

        # Grid vs. Finish Position Change Chart
        st.subheader("📊 Positions Gained / Lost from Grid")
        st.caption("Green indicates positions gained relative to starting grid; red indicates positions lost.")
        grid_fig = historical_grid_vs_finish_chart(results_df)
        if grid_fig:
            st.plotly_chart(grid_fig, use_container_width=True)

        st.divider()

        # Full Race Classification Table
        st.subheader("📋 Complete Race Classification")

        display_columns = [
            "position",
            "number",
            "DriverName",
            "constructorName",
            "grid",
            "points",
            "status",
            "laps",
            "totalRaceTime",
            "fastestLapTime"
        ]

        available_cols = [c for c in display_columns if c in results_df.columns]

        # Rename columns for cleaner presentation
        rename_map = {
            "position": "Pos",
            "number": "No",
            "DriverName": "Driver",
            "constructorName": "Constructor",
            "grid": "Grid",
            "points": "Points",
            "status": "Status",
            "laps": "Laps",
            "totalRaceTime": "Time / Retired",
            "fastestLapTime": "Fastest Lap"
        }

        display_df = results_df[available_cols].rename(columns=rename_map)

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Race Results (CSV)",
            data=csv_data,
            file_name=f"{year}_{grand_prix.replace(' ', '_')}_results.csv",
            mime="text/csv"
        )

    else:
        st.info(f"No race classification results were found for {year} {grand_prix}.")


# =========================================================
# TAB 2: CHAMPIONSHIP STANDINGS
# =========================================================

with tab_standings:
    col_d, col_c = st.columns(2)

    with st.spinner("Fetching championship standings..."):
        driver_standings = get_driver_standings(year)
        constructor_standings = (
            get_constructor_standings(year) if year >= 1958 else pd.DataFrame()
        )

    with col_d:
        st.subheader(f"🥇 {year} Driver Standings")
        if not driver_standings.empty:
            d_fig = historical_standings_chart(
                driver_standings,
                f"{year} Top Drivers by Points"
            )
            if d_fig:
                st.plotly_chart(d_fig, use_container_width=True)

            d_cols = [
                c for c in [
                    "position",
                    "DriverName",
                    "points",
                    "wins"
                ] if c in driver_standings.columns
            ]

            st.dataframe(
                driver_standings[d_cols].rename(
                    columns={
                        "position": "Pos",
                        "DriverName": "Driver",
                        "points": "Points",
                        "wins": "Wins"
                    }
                ),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Driver championship standings are unavailable for this season.")

    with col_c:
        st.subheader(f"🏎️ {year} Constructor Standings")
        if year >= 1958:
            if not constructor_standings.empty:
                c_fig = historical_standings_chart(
                    constructor_standings,
                    f"{year} Top Constructors by Points"
                )
                if c_fig:
                    st.plotly_chart(c_fig, use_container_width=True)

                c_cols = [
                    c for c in [
                        "position",
                        "constructorName",
                        "points",
                        "wins"
                    ] if c in constructor_standings.columns
                ]

                st.dataframe(
                    constructor_standings[c_cols].rename(
                        columns={
                            "position": "Pos",
                            "constructorName": "Constructor",
                            "points": "Points",
                            "wins": "Wins"
                        }
                    ),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("Constructor standings are unavailable for this season.")
        else:
            st.info("The World Constructors' Championship began in 1958.")