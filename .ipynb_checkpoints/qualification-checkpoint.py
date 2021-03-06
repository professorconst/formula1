# Imports
import fastf1
import matplotlib as mpl
import matplotlib.pyplot as plt
from fastf1 import plotting
from timple.timedelta import strftimedelta
from fastf1.core import Laps
import pandas as pd

# Configure matplotlib and f1 plots with this intit
mpl.rcParams['figure.dpi'] = 80
mpl.rcParams['figure.figsize'] = (6, 6)
#fastf1.Cache.enable_cache(r"/Users/Professor/Downloads/f1/cache")
fastf1.plotting.setup_mpl()
fastf1.plotting.setup_mpl(mpl_timedelta_support=True,
                          color_scheme='fastf1',
                          misc_mpl_mods=False)

year = 2021  #GP year
gp = 'Abu Dhabi'  # GP name
event = 'Q'  # Q for qualifying, FP1 for free practice 1, R for race

# Get qualification session
session = fastf1.get_session(year, gp, event)
laps = session.load_laps()
laps.dropna(subset=['Driver'], inplace=True)

# Get an array of all drivers
drivers = pd.unique(laps['Driver'])
print(drivers)

# Get each driver fastest lap
list_fastest_laps = list()
for drv in drivers:
    drvs_fastest_lap = laps.pick_driver(drv).pick_fastest()
    list_fastest_laps.append(drvs_fastest_lap)
fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(
    drop=True)

# Get the pole lap
pole_lap = fastest_laps.pick_fastest()
fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']

print(fastest_laps[['Driver', 'LapTime', 'LapTimeDelta']])

# Get team colors
team_colors = list()
for index, lap in fastest_laps.iterlaps():
    color = fastf1.plotting.team_color(lap['Team'])
    team_colors.append(color)

# Plot the table
fig, ax = plt.subplots()
ax.barh(fastest_laps.index,
        fastest_laps['LapTimeDelta'],
        color=team_colors,
        edgecolor='grey')
ax.set_yticks(fastest_laps.index)
ax.set_yticklabels(fastest_laps['Driver'])
ax.invert_yaxis()
ax.set_axisbelow(True)
ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)

lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')
plt.suptitle(f"{session.weekend.name} {session.weekend.year} Qualifying \n"
             f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")
plt.show()
