from SIR_model import Model

model = Model()
model.run()
model.plot('images\\example_simulation.png')
model.queueDistributionPlot(
    'images\\example_simulation_queue_distribution.png')
