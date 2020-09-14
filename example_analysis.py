from matplotlib import rc
import os
from model import Model
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")

rc('text', usetex=True)

model1 = Model(rateSI=0.01)
model1.run()

model2 = Model(rateSI=0.05)
model2.run()

model3 = Model(rateSI=.1)
model3.run()

t = model1.Results['Time']
plt.plot(t, model1.Results['Infected'])
plt.plot(t, model2.Results['Infected'])
plt.plot(t, model3.Results['Infected'])
plt.legend([r'$\beta = .01$', r'$\beta = .05$', r'$\beta = .10$'])
plt.savefig('example_analysis.png', dpi=300)
plt.close()
os.startfile('example_analysis.png', 'open')
