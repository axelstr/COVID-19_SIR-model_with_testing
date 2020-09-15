from model import Model
import os


def main():
    # model = Model(duration=365*2, timeStep=1, susceptible=1000,
    #               infected=1, removed=0, rateSI=0.05, rateIR=0.01)

    model = Model(duration=40, susceptible=100,
                  infected=10, removed=0, rateSI=.2,
                  servers=0,
                  seed=None)
    model.run()
    model.plot()


if __name__ == '__main__':
    main()
    # os.system('python example_simulation.py')
    # os.system('python example_analysis.py')
