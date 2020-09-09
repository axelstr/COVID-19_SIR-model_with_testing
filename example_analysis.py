from model import Model
import matplotlib.pyplot as plt
import os

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
plt.savefig('example_analysis.png', dpi=300)
plt.close()
os.startfile('example_analysis.png', 'open')
