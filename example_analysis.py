# ------- Import -------
from SIR_model import Model

import os
import sys
import subprocess
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")

# ------- Simulate -------
model1 = Model(servers=1)
model1.run()

model2 = Model(servers=2)
model2.run()

model3 = Model(servers=3)
model3.run()

# ------- Plot -------
fileName = 'images\\example_analysis.png'
plt.subplot(2, 1, 1)
plt.stackplot(model1.Results['Time'],
              [model1.Results['Infected'], model1.Results['Susceptible'],
               model1.Results['Removed']], labels=['Infected', 'Susceptible', 'Removed'],
              colors=['salmon', 'lightgreen', 'dimgray'])
plt.ylabel('1 servers')
plt.legend(bbox_to_anchor=(1.1, 1), loc='right',
           ncol=1, fancybox=True, shadow=True)
plt.tick_params(
    axis='x',
    which='both',
    bottom=False,
    top=False,
    labelbottom=False)
plt.xlim(min(model1.Results['Time']), max(model1.Results['Time']))
plt.ylim(0, model1.TotalIndividuals)
plt.title('Server Analysis')

plt.subplot(2, 1, 2)
plt.stackplot(model2.Results['Time'],
              [model2.Results['Infected'], model2.Results['Susceptible'],
               model2.Results['Removed']],
              colors=['salmon', 'lightgreen', 'dimgray'])
plt.xlabel('days')
plt.ylabel('2 servers')
plt.xlim(min(model2.Results['Time']), max(model2.Results['Time']))
plt.ylim(0, model2.TotalIndividuals)

plt.savefig(fileName, dpi=300)
plt.close()

if sys.platform == "win32":
    os.startfile(fileName, 'open')
else:
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, fileName])
