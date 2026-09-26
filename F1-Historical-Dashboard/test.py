import fastf1

print("Loading F1 session...")

session = fastf1.get_session(
    2024,
    "Monaco",
    "R"
)

session.load()

print("\nSession loaded!")

laps = session.laps

print("\nLap data:")
print(laps.head())

print("\nNumber of rows:")
print(len(laps))

print("Available columns:")
print(laps.columns)

drivers = laps["Driver"].dropna().unique()

print("Drivers:")
print(drivers)


#Leclerc's lap data
leclerc_laps = laps[
    laps["Driver"] == "LEC"
]
print("\nLeclerc's lap data:")
print(leclerc_laps.head())

#hamilton's lap data
hamilton_laps = laps[
    laps["Driver"] == "HAM"
]
print("\nHamilton's lap data:")
print(hamilton_laps.head())

#Leclerc's fastest lap
leclerc_fastest_lap = (
    laps
    .pick_drivers("LEC")
    .pick_fastest()
)

print("\nLeclerc's fastest lap:")
print(leclerc_fastest_lap["LapTime"])

#get telemetry data
telemetry = leclerc_fastest_lap.get_telemetry()
print("\nLeclerc's telemetry data:")
print(telemetry.head())
print("\nLeclerc's telemetry data columns:")
print(telemetry.columns)
