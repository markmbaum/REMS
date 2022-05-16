from os.path import join
from numpy import *
from pandas import *
import matplotlib.pyplot as plt

plt.style.use('dark_background')

#------------------------------------------------------------------------------

#input data directory
dirin = join('..', 'data', 'pro')

#------------------------------------------------------------------------------

df = DataFrame({
    't': fromfile(join(dirin, 't'), dtype=int32),
    'sol': fromfile(join(dirin, 'sol'), dtype=int32),
    'T': fromfile(join(dirin, 'ambient_temp'), dtype=float32),
    'P': fromfile(join(dirin, 'pressure'), dtype=float32),
})

g = df.groupby('sol')
ma = g.max()
me = g.mean()
mi = g.min('sol')

fig, axs = plt.subplots(2, 1, figsize=(8,5), constrained_layout=True)
for ax, c in zip(axs, ('T', 'P')):
    for mm in (ma, me, mi):
        ax.plot(mm.index.values, mm[c])
fig.supxlabel("Sol (Mars Day)")
axs[0].set_ylabel("Temperature [K]")
axs[1].set_ylabel("Pressure [Pa]")
fig.suptitle("Daily Max, Mean, and Min Weather from the Curiosity Rover")
fig.savefig(join('..', 'plots', 'rems_plot.png'), dpi=500)

plt.show()