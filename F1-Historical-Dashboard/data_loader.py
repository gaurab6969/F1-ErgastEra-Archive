import os
import fastf1
from fastf1.ergast import Ergast
import streamlit as st
import pandas as pd

ergast = Ergast()

# =========================================================
# 1. HISTORICAL RACE RESULTS (1950 - Present)
# =========================================================
@st.cache_data(show_spinner=False)
def get_historical_race_results(year, round_number=None):
    """
    Fetch full race results (classification, status, points, grid)
    for any race from 1950 to present.
    """
    res = ergast.get_race_results(season=year, round=round_number)
    if not res.content or len(res.content) == 0:
        return pd.DataFrame()
    
    df = res.content[0]
    # Create a clean Driver name column
    if "givenName" in df.columns and "familyName" in df.columns:
        df["DriverName"] = df["givenName"] + " " + df["familyName"]
    return df


# =========================================================
# 2. DRIVER CHAMPIONSHIP STANDINGS (1950 - Present)
# =========================================================
@st.cache_data(show_spinner=False)
def get_driver_standings(year):
    """
    Fetch final (or current) Driver Championship standings for a season.
    """
    standings = ergast.get_driver_standings(season=year)
    if not standings.content or len(standings.content) == 0:
        return pd.DataFrame()
    
    df = standings.content[0]
    if "givenName" in df.columns and "familyName" in df.columns:
        df["DriverName"] = df["givenName"] + " " + df["familyName"]
    return df


# =========================================================
# 3. CONSTRUCTOR STANDINGS (1958 - Present)
# =========================================================
@st.cache_data(show_spinner=False)
def get_constructor_standings(year):
    """
    Fetch Constructor Championship standings (started in 1958).
    """
    standings = ergast.get_constructor_standings(season=year)
    if not standings.content or len(standings.content) == 0:
        return pd.DataFrame()
    return standings.content[0]


# =========================================================
# ENABLE FASTF1 CACHE
# =========================================================

_CACHE_DIR = os.path.join(os.path.dirname(__file__), ".fastf1_cache")
os.makedirs(_CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(_CACHE_DIR)


# =========================================================
# LOAD A SINGLE SESSION
# =========================================================

@st.cache_resource(show_spinner=False)
def load_session(
    year,
    grand_prix,
    session_type
):
    """
    Load a specific F1 session.
    """

    session = fastf1.get_session(
        year,
        grand_prix,
        session_type
    )

    session.load(weather=False, messages=False)

    # Check if lap data was actually loaded
    if not hasattr(session, "_laps") or session.laps is None or session.laps.empty:
        raise ValueError(
            f"No lap timing data is available for {year} {grand_prix} ({session_type}). "
            "FastF1 only has detailed lap timing and telemetry for completed sessions from 2018 onwards."
        )

    return session


# =========================================================
# GET LAP DATA
# =========================================================

def get_laps(session):
    """
    Return lap data from a loaded session.
    """

    try:
        if hasattr(session, "_laps") and session.laps is not None:
            return session.laps
    except Exception:
        pass

    return pd.DataFrame()


# =========================================================
# GET DRIVERS
# =========================================================

def get_drivers(session):
    """
    Return sorted driver abbreviations.
    """

    try:
        if hasattr(session, "_laps") and session.laps is not None and not session.laps.empty:
            drivers = (
                session.laps["Driver"]
                .dropna()
                .unique()
            )
            return sorted(drivers)
    except Exception:
        pass

    try:
        if hasattr(session, "results") and session.results is not None and not session.results.empty:
            if "Abbreviation" in session.results.columns:
                drivers = session.results["Abbreviation"].dropna().unique()
                return sorted(drivers)
    except Exception:
        pass

    return []


# =========================================================
# GET AVAILABLE RACES FOR A SEASON
# =========================================================

@st.cache_data(show_spinner=False)
def get_race_schedule(year):
    """
    Return the F1 race schedule for a season.

    Uses FastF1's Ergast-compatible interface,
    backed by Jolpica-F1.
    """

    from fastf1.ergast import Ergast

    ergast = Ergast()

    schedule = ergast.get_race_schedule(
        season=year
    )

    return schedule


# =========================================================
# GET RACE NAMES
# =========================================================

def get_race_names(year):
    """
    Return Grand Prix names for a season.
    """

    schedule = get_race_schedule(year)

    if schedule is None or schedule.empty:
        return []

    if "raceName" in schedule.columns:
        return schedule["raceName"].tolist()

    return []


# =========================================================
# GET ROUND NUMBER
# =========================================================

def get_round_number(year, grand_prix):
    """
    Get the round number for a specific Grand Prix in a given year.
    """

    schedule = get_race_schedule(year)

    if schedule is None or schedule.empty:
        return 1

    match = schedule[schedule["raceName"] == grand_prix]

    if not match.empty and "round" in match.columns:
        return int(match["round"].iloc[0])

    return 1