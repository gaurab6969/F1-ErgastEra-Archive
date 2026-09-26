import pandas as pd


def prepare_lap_data(laps):
    """
    Clean and prepare lap data for analysis.
    """

    df = laps.copy()

    # Convert lap time to seconds
    if "LapTime" in df.columns:
        df["LapTimeSeconds"] = (
            df["LapTime"].dt.total_seconds()
        )

    return df


def get_driver_laps(laps, driver):
    """
    Return laps for a selected driver.
    """

    df = laps[
        laps["Driver"] == driver
    ].copy()

    return prepare_lap_data(df)


def get_fastest_lap(laps, driver):
    """
    Return the fastest valid lap of a driver.
    """

    driver_laps = get_driver_laps(
        laps,
        driver
    )

    valid_laps = driver_laps.dropna(
        subset=["LapTimeSeconds"]
    )

    if valid_laps.empty:
        return None

    fastest = valid_laps.loc[
        valid_laps["LapTimeSeconds"].idxmin()
    ]

    return fastest


def get_average_lap_time(laps, driver):
    """
    Calculate average lap time for a driver.
    """

    driver_laps = get_driver_laps(
        laps,
        driver
    )

    valid_times = driver_laps[
        "LapTimeSeconds"
    ].dropna()

    if valid_times.empty:
        return None

    return valid_times.mean()


def get_lap_time_comparison(
    laps,
    driver1,
    driver2
):
    """
    Prepare lap-time data for comparing two drivers.
    """

    d1 = get_driver_laps(
        laps,
        driver1
    )

    d2 = get_driver_laps(
        laps,
        driver2
    )

    d1 = d1[
        ["LapNumber", "LapTimeSeconds"]
    ].copy()

    d2 = d2[
        ["LapNumber", "LapTimeSeconds"]
    ].copy()

    d1["Driver"] = driver1
    d2["Driver"] = driver2

    comparison = pd.concat(
        [d1, d2],
        ignore_index=True
    )

    return comparison


def get_tyre_data(laps, driver):
    """
    Return tyre information for a driver.
    """

    driver_laps = get_driver_laps(
        laps,
        driver
    )

    columns = [
        "LapNumber",
        "Compound",
        "TyreLife",
        "Stint",
        "LapTimeSeconds"
    ]

    available_columns = [
        col for col in columns
        if col in driver_laps.columns
    ]

    return driver_laps[
        available_columns
    ].dropna(
        subset=["LapTimeSeconds"]
    )


def get_stint_summary(laps, driver):
    """
    Calculate basic stint statistics.
    """

    driver_laps = get_driver_laps(
        laps,
        driver
    )

    if "Stint" not in driver_laps.columns:
        return pd.DataFrame()

    summary = (
        driver_laps
        .dropna(subset=["LapTimeSeconds"])
        .groupby(
            ["Stint", "Compound"],
            dropna=False
        )
        .agg(
            StartLap=("LapNumber", "min"),
            EndLap=("LapNumber", "max"),
            Laps=("LapNumber", "count"),
            AverageLapTime=("LapTimeSeconds", "mean"),
            BestLapTime=("LapTimeSeconds", "min")
        )
        .reset_index()
    )

    return summary


def calculate_tyre_degradation(
    laps,
    driver
):
    """
    Estimate lap-time change as tyre age increases.

    A simple linear regression is used:
    
    Lap Time = slope * Tyre Life + intercept

    Positive slope generally indicates lap time
    increasing as the tyre gets older.
    """

    tyre_data = get_tyre_data(
        laps,
        driver
    )

    if (
        "TyreLife" not in tyre_data.columns
        or tyre_data.empty
    ):
        return None

    data = tyre_data.dropna(
        subset=[
            "TyreLife",
            "LapTimeSeconds"
        ]
    )

    if len(data) < 2:
        return None

    x = data["TyreLife"]
    y = data["LapTimeSeconds"]

    slope, intercept = (
        __import__("numpy")
        .polyfit(x, y, 1)
    )

    return {
        "slope": slope,
        "intercept": intercept
    }


def get_position_data(laps, driver):
    """
    Return position progression for a driver.
    """

    driver_laps = get_driver_laps(
        laps,
        driver
    )

    if "Position" not in driver_laps.columns:
        return pd.DataFrame()

    return driver_laps[
        [
            "LapNumber",
            "Position"
        ]
    ].dropna()


def get_driver_statistics(laps, driver):
    """
    Return important summary statistics.
    """

    driver_laps = get_driver_laps(
        laps,
        driver
    )

    fastest = get_fastest_lap(
        laps,
        driver
    )

    average = get_average_lap_time(
        laps,
        driver
    )

    result = {
        "driver": driver,
        "laps": len(driver_laps),
        "average_lap": average,
        "fastest_lap": None
    }

    if fastest is not None:
        result["fastest_lap"] = (
            fastest["LapTimeSeconds"]
        )

    return result