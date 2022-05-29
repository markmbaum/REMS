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
df = read_feather(join(dirin, 'rems.feather'))
print('data loaded')

#max, mean, min temperature and pressure
fig, axs = plt.subplots(2, 1, constrained_layout=True)
g = df.groupby('sol')
ma = g.max()
me = g.mean()
mi = g.min('sol')
colors = ('C0', 'C4', 'C9')
for ax, c in zip(axs, ('ambient_temp', 'pressure')):
    for mm, label, color in zip((ma, me, mi), ('max', 'mean', 'min'), colors):
        ax.plot(mm.index.values, mm[c], color=color, label=label)
fig.supxlabel("Sol (Mars Day)")
axs[0].set_ylabel("Temperature [K]")
axs[1].set_ylabel("Pressure [Pa]")
axs[1].legend()
fig.suptitle("Daily Max, Mean, and Min Weather from the Curiosity Rover")
savefig(fig, 'daily_stats')

#P & T histogram
fig, ax = plt.subplots(1, 1, constrained_layout=True)
histplot(df, x='ambient_temp', y='pressure', cmap='magma', ax=ax)
ax.set_xlabel('Temperature [K]')
ax.set_ylabel('Pressure [Pa]')
savefig(fig, 'P_T_histogram')

plt.close('all')