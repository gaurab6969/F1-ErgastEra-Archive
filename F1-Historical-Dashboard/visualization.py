import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def lap_time_chart(
    comparison_data
):
    """
    Create a lap-time comparison chart.
    """

    fig = px.line(
        comparison_data,
        x="LapNumber",
        y="LapTimeSeconds",
        color="Driver",
        markers=True,
        title="Lap Time Comparison"
    )

    fig.update_layout(
        xaxis_title="Lap Number",
        yaxis_title="Lap Time (seconds)",
        hovermode="x unified"
    )

    return fig


def tyre_degradation_chart(
    tyre_data
):
    """
    Create a tyre degradation chart.
    """

    if tyre_data.empty:
        return None

    fig = px.scatter(
        tyre_data,
        x="TyreLife",
        y="LapTimeSeconds",
        color="Compound",
        hover_data=[
            "LapNumber",
            "Stint"
        ],
        title="Tyre Performance / Degradation"
    )

    fig.update_layout(
        xaxis_title="Tyre Life (laps)",
        yaxis_title="Lap Time (seconds)"
    )

    return fig


def position_chart(
    position_data,
    driver
):
    """
    Create a driver position progression chart.
    """

    if position_data.empty:
        return None

    fig = px.line(
        position_data,
        x="LapNumber",
        y="Position",
        markers=True,
        title=f"{driver} Position Progression"
    )

    # F1 position 1 should appear at the top
    fig.update_yaxes(
        autorange="reversed"
    )

    fig.update_layout(
        xaxis_title="Lap Number",
        yaxis_title="Position"
    )

    return fig


def stint_chart(
    stint_data
):
    """
    Create average lap-time chart by stint.
    """

    if stint_data.empty:
        return None

    stint_data = stint_data.copy()

    stint_data["StintLabel"] = (
        "Stint "
        + stint_data["Stint"].astype(str)
        + " - "
        + stint_data["Compound"].astype(str)
    )

    fig = px.bar(
        stint_data,
        x="StintLabel",
        y="AverageLapTime",
        title="Average Lap Time by Stint",
        text_auto=".2f"
    )

    fig.update_layout(
        xaxis_title="Stint",
        yaxis_title="Average Lap Time (seconds)"
    )

    return fig


def telemetry_chart(
    telemetry,
    y_column,
    title,
    y_axis_title
):
    """
    Create a telemetry chart.

    telemetry should contain:
    Distance
    and the selected telemetry variable.
    """

    if telemetry is None or telemetry.empty:
        return None

    if "Distance" not in telemetry.columns:
        return None

    if y_column not in telemetry.columns:
        return None

    fig = px.line(
        telemetry,
        x="Distance",
        y=y_column,
        title=title
    )

    fig.update_layout(
        xaxis_title="Distance (m)",
        yaxis_title=y_axis_title
    )

    return fig


def track_map(
    telemetry
):
    """
    Create an XY track map from telemetry.
    """

    if telemetry is None or telemetry.empty:
        return None

    required = [
        "X",
        "Y"
    ]

    if not all(
        column in telemetry.columns
        for column in required
    ):
        return None

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=telemetry["X"],
            y=telemetry["Y"],
            mode="lines",
            name="Racing Line"
        )
    )

    fig.update_layout(
        title="Track Map",
        xaxis_title="X",
        yaxis_title="Y",
        yaxis_scaleanchor="x",
        showlegend=False
    )

    return fig


def historical_grid_vs_finish_chart(
    results_df
):
    """
    Create a chart showing positions gained/lost from starting grid.
    """

    if results_df.empty:
        return None

    df = results_df.copy()

    df["position"] = pd.to_numeric(df["position"], errors="coerce")
    df["grid"] = pd.to_numeric(df["grid"], errors="coerce")

    df = df.dropna(subset=["position", "grid"])

    if df.empty:
        return None

    df["PositionsGained"] = df["grid"] - df["position"]

    driver_col = "DriverName" if "DriverName" in df.columns else "driverId"

    df["ChangeStatus"] = df["PositionsGained"].apply(
        lambda x: "Gained" if x > 0 else ("Lost" if x < 0 else "Maintained")
    )

    color_map = {
        "Gained": "#2ecc71",
        "Lost": "#e74c3c",
        "Maintained": "#95a5a6"
    }

    fig = px.bar(
        df.sort_values(by="position", ascending=True),
        x="PositionsGained",
        y=driver_col,
        orientation="h",
        color="ChangeStatus",
        color_discrete_map=color_map,
        title="Positions Gained / Lost from Grid",
        hover_data=["grid", "position", "constructorName"] if "constructorName" in df.columns else ["grid", "position"]
    )

    fig.update_layout(
        xaxis_title="Positions Gained (+) / Lost (-)",
        yaxis_title="Driver",
        yaxis={"autorange": "reversed"}
    )

    return fig


def historical_standings_chart(
    standings_df,
    title="Championship Standings"
):
    """
    Create a horizontal bar chart of top drivers or constructors by points.
    """

    if standings_df.empty:
        return None

    df = standings_df.copy()

    df["points"] = pd.to_numeric(df["points"], errors="coerce").fillna(0)
    df = df.head(15).sort_values(by="points", ascending=True)

    name_col = (
        "DriverName" if "DriverName" in df.columns
        else ("constructorName" if "constructorName" in df.columns
        else ("name" if "name" in df.columns else "driverId"))
    )

    fig = px.bar(
        df,
        x="points",
        y=name_col,
        orientation="h",
        title=title,
        text="points",
        color="points",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        xaxis_title="Championship Points",
        yaxis_title="Driver / Constructor",
        showlegend=False
    )

    return fig