import fastf1
from fastf1 import plotting
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

# Enable FastF1 cache to store data locally
fastf1.Cache.enable_cache('cache/')

# Load 2023 Monaco Grand Prix, Qualifying session
session = fastf1.get_session(2023, 'Monaco', 'Q')
session.load()

# Get lap data for two drivers
driver1 = 'VER'  # Verstappen
driver2 = 'HAM'  # Hamilton
laps_driver1 = session.laps.pick_driver(driver1)
laps_driver2 = session.laps.pick_driver(driver2)

# Get telemetry for fastest laps
fastest_driver1 = laps_driver1.pick_fastest()
fastest_driver2 = laps_driver2.pick_fastest()
telemetry_driver1 = fastest_driver1.get_telemetry()
telemetry_driver2 = fastest_driver2.get_telemetry()

telemetry_driver1['Distance'] = telemetry_driver1['Distance']
telemetry_driver2['Distance'] = telemetry_driver2['Distance']

# Calculate time delta between drivers
delta_time = telemetry_driver1['Time'] - telemetry_driver2['Time']

# Print lap times for comparison
print(f"{driver1} Fastest Lap: {fastest_driver1['LapTime']}")
print(f"{driver2} Fastest Lap: {fastest_driver2['LapTime']}")

# Set up FastF1 plotting style
plotting.setup_mpl()

# Plot speed traces
plt.figure(figsize=(10, 6))
plt.plot(telemetry_driver1['Distance'], telemetry_driver1['Speed'], label=f'{driver1}', color='red')
plt.plot(telemetry_driver2['Distance'], telemetry_driver2['Speed'], label=f'{driver2}', color='blue')
plt.title('Speed Trace Comparison - Monaco 2023 Qualifying')
plt.xlabel('Distance (m)')
plt.ylabel('Speed (km/h)')
plt.legend()
plt.grid()
plt.savefig('speed_trace.png')
plt.show()

# Plot throttle inputs
plt.figure(figsize=(10, 6))
plt.plot(telemetry_driver1['Distance'], telemetry_driver1['Throttle'], label=f'{driver1}', color='red')
plt.plot(telemetry_driver2['Distance'], telemetry_driver2['Throttle'], label=f'{driver2}', color='blue')
plt.title('Throttle Input Comparison - Monaco 2023 Qualifying')
plt.xlabel('Distance (m)')
plt.ylabel('Throttle (%)')
plt.legend()
plt.grid()
plt.savefig('throttle_comparison.png')
plt.show()

# Calculate sector times (if available)
sector1_driver1 = fastest_driver1['Sector1Time']
sector1_driver2 = fastest_driver2['Sector1Time']
print(f"Sector 1: {driver1} {sector1_driver1}, {driver2} {sector1_driver2}")

# Interactive speed plot
fig = px.line(telemetry_driver1, x='Distance', y='Speed', title=f'{driver1} Speed Trace')
fig.add_scatter(x=telemetry_driver2['Distance'], y=telemetry_driver2['Speed'], name=driver2)
fig.write_xaxes(title='Distance (m)')
fig.update_yaxes(title='Speed (km/h)')
fig.write({'title': 'Speed Trace Comparison - Monaco 2023'})
fig.write_html('speed_trace_interactive.html')