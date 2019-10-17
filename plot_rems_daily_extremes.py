import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('dark_background')

#-------------------------------------------------------------------------------
#INPUT

assert len(sys.argv) > 1, 'the processed data file name must be specified at cmd line'
fncsv = sys.argv[1]

#-------------------------------------------------------------------------------
#FUNCTIONS

def nan_outliers(df, col, stds=2.5):
    std = df[col].std()
    mean = df[col].mean()
    for idx in df.index:
        if df.at[idx,col] > mean + stds*std or df.at[idx,col] < mean - stds*std:
            df.at[idx,col] = np.nan

#-------------------------------------------------------------------------------
#MAIN

#load data
df = pd.read_csv(fncsv)

#remove outliers
nan_outliers(df, 'AMBIENT_TEMP_min')
nan_outliers(df, 'AMBIENT_TEMP_max')
nan_outliers(df, 'PRESSURE_min')
nan_outliers(df, 'PRESSURE_max')

#init plotting objects
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,6))

#plot surface temperature
ax1.plot(df.SOL, df.AMBIENT_TEMP_max, '.', markersize=1, label='Max Temp')
ax1.plot(df.SOL, df.AMBIENT_TEMP_min, '.', markersize=1, label='Min Temp')
sol = 669
count = 1
lim = [df.AMBIENT_TEMP_min.min(), df.AMBIENT_TEMP_max.max()]
lim[1] -= 0.05*(lim[1] - lim[0])
while(sol < df.SOL.max()):
    ax1.plot([sol]*2, lim, '--', color='gray')
    if(sol == 669):
        ax1.text(sol, max(lim), '1 Mars Year', ha='center', va='bottom', fontsize=9)
    else:
        ax1.text(sol, max(lim), '%d Mars Years' % count, ha='center', va='bottom', fontsize=9)
    count += 1
    sol += 669
ax1.set_ylabel('Daily Surface\nAir Temperature (K)')
ax1.legend()
ax1.grid(True, alpha=0.1)

#plot surface pressure
ax2.plot(df.SOL, df.PRESSURE_max, '.', color='C2', markersize=1.5, label='Max Pressure')
ax2.plot(df.SOL, df.PRESSURE_min, '.', color='C3', markersize=1.5, label='Min Pressure')
sol = 669
lim = [df.PRESSURE_min.min(), df.PRESSURE_max.max()]
while(sol < df.SOL.max()):
    ax2.plot([sol]*2, lim, '--', color='gray')
    sol += 669
ax2.set_ylabel('Daily Surface\nPressure (Pa)')
ax2.set_xlabel('Sol (Mars Day)')
ax2.legend()
ax2.grid(True, alpha=0.1)

#save
fig.suptitle('Curiosity Rover Temperature and Pressure\n(Outliers Removed)')
plt.savefig('rems_plot', transparent=False)
plt.savefig('rems_plot.pdf', fmt='pdf', transparent=False)
plt.show()
