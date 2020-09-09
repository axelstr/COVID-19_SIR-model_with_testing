from model import Model

model = Model(duration=365, servers=0)
model.run()
model.plot('example_simulation.png')
