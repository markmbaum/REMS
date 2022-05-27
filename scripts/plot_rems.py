from os.path import join
from numpy import *
from pandas import *
import matplotlib.pyplot as plt
from seaborn import *

#------------------------------------------------------------------------------

#input data directory
dirin = join('..', 'data', 'pro')

#output plots directory
dirplots = join('..', 'plots')

#------------------------------------------------------------------------------

def savefig(fig, fn):
    p = join(dirplots, fn)
    fig.savefig(p, dpi=500)
    print('plot saved:', p)
    return(None)

#------------------------------------------------------------------------------

#load data
df = DataFrame({
    't': fromfile(join(dirin, 't_int32'), dtype=int32),
    'sol': fromfile(join(dirin, 'sol_int32'), dtype=int32),
    'T': fromfile(join(dirin, 'ambient_temp_float32'), dtype=float32),
    'P': fromfile(join(dirin, 'pressure_float32'), dtype=float32),
})
#df = df.dropna()
print('data loaded')

#P & T histogram
fig, ax = plt.subplots(1, 1, constrained_layout=True)
histplot(df, x='T', y='P', cmap='magma', ax=ax)
ax.set_xlabel('Temperature [K]')
ax.set_ylabel('Pressure [Pa]')
savefig(fig, 'P_T_histogram')

#max, mean, min temperature and pressure
fig, axs = plt.subplots(2, 1, constrained_layout=True)
g = df.groupby('sol')
ma = g.max()
me = g.mean()
mi = g.min('sol')
for ax, c in zip(axs, ('T', 'P')):
    for mm, label in zip((ma, me, mi), ('max', 'mean', 'min')):
        ax.plot(mm.index.values, mm[c], label=label)
fig.supxlabel("Sol (Mars Day)")
axs[0].set_ylabel("Temperature [K]")
axs[0].legend()
axs[1].set_ylabel("Pressure [Pa]")
axs[1].legend()
fig.suptitle("Daily Max, Mean, and Min Weather from the Curiosity Rover")
savefig(fig, 'daily_stats')

plt.show()